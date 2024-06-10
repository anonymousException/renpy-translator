import _thread
import os
import subprocess
import threading
import time
import traceback

from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtWidgets import QDialog, QFileDialog

from my_log import log_print
from html_util import open_directory_and_select_file
from extraction_official import Ui_ExtractionOfficialDialog
from call_game_python import get_python_path_from_game_path, get_py_path
import my_log


class extractThread(threading.Thread):
    def __init__(self, path, tl_name, is_gen_empty, is_show_directory):
        threading.Thread.__init__(self)
        self.path = path
        self.tl_name = tl_name
        self.is_gen_empty = is_gen_empty
        self.is_show_directory = is_show_directory

    def run(self):
        try:
            tl_name = self.tl_name
            is_gen_empty = self.is_gen_empty
            is_show_directory = self.is_show_directory
            log_print('start official extraction ...')
            exec_official_translate(self.path, tl_name, is_gen_empty)
            log_print('official extraction complete!')
            if is_show_directory:
                show_dir = os.path.dirname(self.path) + '/game/tl/' + tl_name
                open_directory_and_select_file(show_dir)

        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


class MyExtractionOfficialForm(QDialog, Ui_ExtractionOfficialDialog):
    def __init__(self, parent=None):
        super(MyExtractionOfficialForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.extractBtn.clicked.connect(self.extract)
        self.extract_thread = None
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
                self.extract_thread = t
                t.start()
                self.setDisabled(True)
                self.extractBtn.setText(QCoreApplication.translate('MainWindow', 'is extracting...', None))

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('ExtractionOfficialDialog',
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
            if self.extract_thread is not None:
                if not self.extract_thread.is_alive():
                    self.extractBtn.setText(QCoreApplication.translate('MainWindow', 'extract', None))
                    self.setEnabled(True)
                    self.extract_thread = None

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


def get_translate_cmd(game_path, tl_name):
    python_path = get_python_path_from_game_path(game_path)
    py_path = get_py_path(game_path)
    game_dir = os.path.dirname(game_path)
    command = '"' + python_path + '"' + ' -O "' + py_path + '" "' + game_dir + '" translate "' + tl_name + '"'
    return command


def exec_official_translate(game_path, tl_name, is_gen_empty):
    command = get_translate_cmd(game_path, tl_name)
    if is_gen_empty:
        command = command + ' --empty'
    log_print(command)
    p = subprocess.Popen(command, shell=True, stdout=my_log.f, stderr=my_log.f,
                         creationflags=0x08000000, text=True, encoding='utf-8')
    p.wait()
