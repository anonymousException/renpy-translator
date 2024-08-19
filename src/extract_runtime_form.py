import _thread
import io
import json
import os
import shutil
import subprocess
import threading
import time
import traceback

from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtWidgets import QDialog, QFileDialog

from extraction_runtime import Ui_ExtractionRuntimeDialog
from my_log import log_print
from html_util import open_directory_and_select_file
from string_tool import encode_say_string

hook_script = 'hook_extract.rpy'
hooked_result = 'extraction_hooked.json'
extract_finish = 'extract_runtime.finish'


def get_line_number(element):
    return element[3]


class extractThread(threading.Thread):
    def __init__(self, path, tl_name, is_gen_empty, is_show_directory):
        threading.Thread.__init__(self)
        self.path = path
        self.tl_name = tl_name
        self.is_gen_empty = is_gen_empty
        self.is_show_directory = is_show_directory

    def run(self):
        try:
            if os.path.isfile(extract_finish):
                os.remove(extract_finish)
            path = self.path
            tl_name = self.tl_name
            is_gen_empty = self.is_gen_empty
            dir = os.path.dirname(path)
            target = dir + '/game/' + hook_script
            shutil.copyfile(hook_script, target)
            command = 'start "" /wait /d "' + dir + '"  "' + path + '"'
            self.path = path
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 creationflags=0x08000000, text=True, encoding='utf-8')
            p.wait()

            target = dir + '/' + hooked_result
            while True:
                if os.path.isfile(target) and os.path.getsize(target) > 0:
                    target = dir + '/game/' + hook_script
                    if os.path.exists(target):
                        os.remove(target)
                    target = target + 'c'
                    if os.path.exists(target):
                        os.remove(target)
                    target = dir + '/' + hooked_result
                    break
                time.sleep(1)
            if os.path.isfile(target):
                f = io.open(target, 'r', encoding='utf-8')
                dic = json.load(f)
                f.close()
                os.remove(target)
                for key, value in dic.items():
                    value.sort(key=get_line_number)
                    if key.startswith('game/'):
                        target = key[:5] + 'tl/' + tl_name + '/' + key[5:]
                    else:
                        target = 'game/tl/' + tl_name + '/' + key
                    target = dir + '/' + target
                    target_dir = os.path.dirname(target)
                    target = os.path.splitext(target)[0] + '.rpy'
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir, exist_ok=True)
                    if not os.path.isfile(target):
                        f = io.open(target, 'w', encoding='utf-8')
                        for i in value:
                            identifier = i[0]
                            who = i[1]
                            what = i[2]
                            what = encode_say_string(what)
                            linenumber = i[3]
                            f.write(f'\n# game/{key}:{linenumber}\n')
                            f.write(f'translate {tl_name} {identifier}:\n')
                            f.write('\n')
                            if who is not None:
                                who = who + ' '
                            else:
                                who = ''
                            f.write(f'    # {who}"{what}"\n')
                            if is_gen_empty:
                                f.write(f'    {who}""\n')
                            else:
                                f.write(f'    {who}"{what}"\n')
                            # print(f'who:{who} what:{what} {key} {linenumber}')
                        f.close()
                    else:
                        f = io.open(target, 'r', encoding='utf-8')
                        _read_lines = f.readlines()
                        f.close()
                        identifier_sets = set()
                        for i in _read_lines:
                            if i.startswith(f'translate {tl_name} '):
                                identifier = i[len(f'translate {tl_name} '):].rstrip('\n').rstrip(':')
                                identifier_sets.add(identifier)
                        f = io.open(target, 'a', encoding='utf-8')
                        f.write('\n')
                        for i in value:
                            identifier = i[0]
                            if identifier in identifier_sets:
                                continue
                            who = i[1]
                            what = i[2]
                            what = encode_say_string(what)
                            linenumber = i[3]
                            f.write(f'\n# game/{key}:{linenumber}\n')
                            f.write(f'translate {tl_name} {identifier}:\n')
                            f.write('\n')
                            if who is not None:
                                who = who + ' '
                            else:
                                who = ''
                            f.write(f'    # {who}"{what}"\n')
                            if is_gen_empty:
                                f.write(f'    {who}""\n')
                            else:
                                f.write(f'    {who}"{what}"\n')
                            # print(f'who:{who} what:{what} {key} {linenumber}')
                        f.close()
                if self.is_show_directory:
                    open_directory_and_select_file(target)
                log_print('runtime extract complete!')
                f = io.open(extract_finish, 'w', encoding='utf-8')
                f.close()
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            f = io.open(extract_finish, 'w', encoding='utf-8')
            f.close()


class MyExtractionRuntimeForm(QDialog, Ui_ExtractionRuntimeDialog):
    def __init__(self, parent=None):
        super(MyExtractionRuntimeForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.extractBtn.clicked.connect(self.extract)
        _thread.start_new_thread(self.update, ())

    def extract(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        tl_name = self.tlNameText.toPlainText().strip('\n').strip()
        if len(tl_name) == 0:
            log_print('tl_name should not be empty')
            return
        if os.path.isfile(path):
            if path.endswith('.exe'):
                t = extractThread(path, tl_name, self.emptyCheckBox.isChecked(), True)
                t.start()
                self.setDisabled(True)

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('ExtractionRuntimeDialog',
                                                                                'select the game file you want to extract',
                                                                                None),
                                                     '',
                                                     "Game Files (*.exe)")
        self.selectFileText.setText(file)

    def update(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self):
        try:
            if not self.isEnabled():
                if os.path.isfile(extract_finish):
                    os.remove(extract_finish)
                    if not os.path.isfile(extract_finish):
                        self.setEnabled(True)

        except Exception:
            msg = traceback.format_exc()
            log_print(msg)

    class UpdateThread(QThread):
        update_date = Signal()

        def __init__(self):
            super().__init__()

        def __del__(self):
            self.wait()

        def run(self):
            self.update_date.emit()
