import _thread
import io
import json
import os
import queue
import shutil
import time
import traceback

from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from one_key_translate import Ui_OneKeyTranslateDialog
from custom_engine_form import sourceDic, targetDic
from my_log import log_print
from renpy_translate import engineDic, language_header, translateThread, translate_threads
from engine_form import MyEngineForm
from game_unpacker_form import bat, expand_file, finish_flag
from extract_runtime_form import extract_finish
import extract_runtime_form
import renpy_extract
from renpy_fonts import GenGuiFonts
import game_unpacker_form
import add_change_language_entrance_form
from extraction_official_form import exec_official_translate
import extraction_official_form
from font_util import get_default_font_path


class MyQueue(queue.Queue):
    def peek(self):
        """Return the first element in the queue without removing it."""
        with self.mutex:
            return self.queue[0]


q = MyQueue()
qDic = dict()


class MyOneKeyTranslateForm(QDialog, Ui_OneKeyTranslateDialog):
    def __init__(self, parent=None):
        super(MyOneKeyTranslateForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.init_combobox()
        self.changeTranslationEngineButton.clicked.connect(self.show_engine_settings)
        self.local_glossary = None
        self.localGlossaryCheckBox.clicked.connect(self.on_local_glossary_checkbox_state_changed)
        self.selectFontBtn.clicked.connect(self.select_font)
        self.startButton.clicked.connect(self.on_start_button_clicked)
        self.path = None
        self.official_extract_thread = None
        default_font = get_default_font_path()
        if default_font is not None:
            self.selectFontText.setText(default_font)
        _thread.start_new_thread(self.update, ())

    def on_start_button_clicked(self):
        global q, qDic
        q = MyQueue()
        qDic = dict()
        if self.unpackCheckBox.isChecked():
            q.put(self.unpack)
            qDic[self.unpack] = False
        if self.runtimeExtractionCheckBox.isChecked():
            q.put(self.runtime_extract)
            qDic[self.runtime_extract] = False
        if self.officialExtractionCheckBox.isChecked():
            q.put(self.official_extract)
            qDic[self.official_extract] = False
        if self.extractionCheckBox.isChecked():
            q.put(self.extract)
            qDic[self.extract] = False
        if self.replaceFontCheckBox.isChecked():
            q.put(self.replaceFont)
            qDic[self.replaceFont] = False
        if self.addEntranceCheckBox.isChecked():
            q.put(self.add_entrance)
            qDic[self.add_entrance] = False
        if self.translateCheckBox.isChecked():
            q.put(self.translate)
            qDic[self.translate] = False

    def official_extract(self):
        select_file = self.selectFileText.toPlainText()
        if len(select_file) > 0:
            select_file = select_file.replace('file:///', '')
            tl_name = self.tlNameText.toPlainText()
            if len(tl_name) == 0:
                log_print('tl_name should not be empty!')
                qDic[self.official_extract] = True
                return
            if os.path.isfile(select_file):
                if select_file.endswith('.exe'):
                    t = extraction_official_form.extractThread(select_file, tl_name, False, False)
                    self.official_extract_thread = t
                    t.start()
                    self.setDisabled(True)

    def translate(self):
        select_file = self.selectFileText.toPlainText()
        if len(select_file) > 0:
            select_file = select_file.replace('file:///', '')
            tl_name = self.tlNameText.toPlainText()
            if len(tl_name) == 0:
                log_print('tl_name should not be empty!')
                qDic[self.translate] = True
                return
            select_dir = os.path.dirname(select_file) + '/game/tl/' + tl_name
            if not os.path.exists(select_dir):
                log_print(select_dir + ' directory does not exist!')
                qDic[self.translate] = True
            else:
                if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                    select_dir = select_dir + '/'
                paths = os.walk(select_dir, topdown=False)
                cnt = 0
                target_language = targetDic[self.targetComboBox.currentText()]
                source_language = sourceDic[self.sourceComboBox.currentText()]
                for path, dir_lst, file_lst in paths:
                    for file_name in file_lst:
                        i = os.path.join(path, file_name)
                        if not file_name.endswith("rpy"):
                            continue
                        t = translateThread(cnt, i, target_language, source_language,
                                            True,
                                            False, self.local_glossary, True,
                                            True)
                        translate_threads.append(t)
                        cnt = cnt + 1
                if len(translate_threads) > 0:
                    qDic[self.translate] = False
                    for t in translate_threads:
                        t.start()
                    self.setDisabled(True)
                    _thread.start_new_thread(self.translate_threads_over, ())
                else:
                    qDic[self.translate] = True
        else:
            qDic[self.translate] = True

    def translate_threads_over(self):
        for t in translate_threads:
            if t.is_alive():
                t.join()
            translate_threads.remove(t)
        translate_threads.clear()
        log_print('translate all complete!')
        qDic[self.translate] = True
        self.setEnabled(True)

    def add_entrance(self):
        target = self.get_add_entrance_target()
        if target is not None:
            shutil.copyfile(add_change_language_entrance_form.hook_script, target)
            log_print('add entrance success!')
        qDic[self.add_entrance] = True

    def get_add_entrance_target(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                target = os.path.dirname(path)
                target = target + '/game'
                if os.path.isdir(target):
                    target = target + '/' + add_change_language_entrance_form.hook_script
                    return target
        return None

    def replaceFont(self):
        select_file = self.selectFileText.toPlainText()
        if len(select_file) > 0:
            select_file = select_file.replace('file:///', '')
            tl_name = self.tlNameText.toPlainText()
            if len(tl_name) == 0:
                log_print('tl_name should not be empty!')
                qDic[self.replaceFont] = True
                return
            select_dir = os.path.dirname(select_file) + '/game/tl/' + tl_name
            if not os.path.exists(select_dir):
                log_print(select_dir + ' directory does not exist!')
            else:
                if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                    select_dir = select_dir + '/'
                font_path = self.selectFontText.toPlainText()
                font_path = font_path.replace('file:///', '')
                GenGuiFonts(select_dir, font_path)
        qDic[self.replaceFont] = True

    def extract(self):
        # noinspection PyBroadException
        try:
            select_file = self.selectFileText.toPlainText()
            if len(select_file) > 0:
                select_file = select_file.replace('file:///', '')
                tl_name = self.tlNameText.toPlainText()
                if len(tl_name) == 0:
                    log_print('tl_name should not be empty!')
                    qDic[self.extract] = True
                    return
                select_dir = os.path.dirname(select_file) + '/game/tl/' + tl_name
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    t = renpy_extract.extractThread(threadID=0, p=None, tl_name=tl_name, dir=None, tl_dir=select_dir,
                                                    is_open_filter=self.filterCheckBox.isChecked(),
                                                    filter_length=int(self.filterLengthLineEdit.text()),
                                                    is_gen_empty=False)
                    renpy_extract.extract_threads.append(t)

            if len(renpy_extract.extract_threads) > 0:
                qDic[self.extract] = False
                for t in renpy_extract.extract_threads:
                    t.start()
                self.setDisabled(True)
                _thread.start_new_thread(self.extract_threads_over, ())
            else:
                qDic[self.extract] = True
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            qDic[self.extract] = True

    def extract_threads_over(self):
        for t in renpy_extract.extract_threads:
            if t.is_alive():
                t.join()
            renpy_extract.extract_threads.remove(t)
        renpy_extract.extract_threads.clear()
        log_print('extract all complete!')
        qDic[self.extract] = True
        self.setEnabled(True)

    def runtime_extract(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        tl_name = self.tlNameText.toPlainText().strip('\n').strip()
        if len(tl_name) == 0:
            log_print('tl_name should not be empty')
            qDic[self.runtime_extract] = True
            return
        if os.path.isfile(path):
            if path.endswith('.exe'):
                t = extract_runtime_form.extractThread(path, tl_name, False, False)
                t.start()
                self.setDisabled(True)
                return
        qDic[self.runtime_extract] = True

    def closeEvent(self, event):
        self.parent.widget.show()
        self.parent.menubar.show()
        self.parent.versionLabel.show()
        self.parent.actionone_key_translate.triggered.connect(lambda: self.parent.show_one_key_translate_form())
        self.parent.showNormal()
        self.hide()
        event.ignore()
        return

    def clean(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                hook_script_path = dir + '/game/' + game_unpacker_form.hook_script
                if os.path.isfile(hook_script_path):
                    os.remove(hook_script_path)
                if os.path.isfile(hook_script_path + 'c'):
                    os.remove(hook_script_path + 'c')
                bat_path = dir + '/' + bat
                if os.path.isfile(bat_path):
                    os.remove(bat_path)
                expand_path = dir + '/' + expand_file
                if os.path.isfile(expand_path):
                    os.remove(expand_path)

    def unpack(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)

                shutil.copyfile(bat, dir + '/' + bat)
                shutil.copyfile(expand_file, dir + '/' + expand_file)

                shutil.copyfile(game_unpacker_form.hook_script, dir + '/game/' + game_unpacker_form.hook_script)
                command = 'start "" /d "' + dir + '"  "' + path + '"'
                self.path = path
                f = io.open(dir + finish_flag, 'w')
                f.write('waiting')
                f.close()
                self.setDisabled(True)
                os.system(command)
                return
        qDic[self.unpack] = True

    def select_font(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate("FontReplaceDialog",
                                                                                "select the file font which supports the translated language",
                                                                                None),
                                                     '',  # 起始路径
                                                     "Font Files (*.ttf || *.otf);;All Files (*)")
        self.selectFontText.setText(file)

    def on_local_glossary_checkbox_state_changed(self):
        self.local_glossary = None
        if self.localGlossaryCheckBox.isChecked():
            local_glossary_form = self.parent.local_glossary_form
            local_glossary_form.exec()
            dic = local_glossary_form.data
            index = self.sourceComboBox.findText('Auto Detect')
            if dic is None or len(dic) == 0:
                self.localGlossaryCheckBox.setChecked(False)
                if 'Auto Detect' in sourceDic.keys() and index == -1:
                    self.sourceComboBox.addItem('Auto Detect')
                    index = self.sourceComboBox.findText('Auto Detect')
                    self.sourceComboBox.setCurrentIndex(index)
            else:
                if index != -1:
                    current_index = self.sourceComboBox.currentIndex()
                    self.sourceComboBox.removeItem(index)
                    if current_index == index:
                        self.sourceComboBox.setCurrentIndex(0)
                self.local_glossary = dic
        else:
            index = self.sourceComboBox.findText('Auto Detect')
            if 'Auto Detect' in sourceDic.keys() and index == -1:
                self.sourceComboBox.addItem('Auto Detect')
                index = self.sourceComboBox.findText('Auto Detect')
                self.sourceComboBox.setCurrentIndex(index)

    def show_engine_settings(self):
        engine_form = MyEngineForm(parent=self)
        ori = None
        now = None
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                ori = json.load(json_file)
        engine_form.exec()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                now = json.load(json_file)
        if (now is not None and ori is not None and now['engine'] != ori['engine']) \
                or (now is None and ori is None) \
                or (now is not None and ori is None):
            self.init_combobox()

    @staticmethod
    def get_combobox_content(p, d):
        if not os.path.isfile(p):
            return []
        try:
            f = io.open(p, 'r', encoding='utf-8')
            _read = f.read()
            f.close()
            _read_line = _read.split('\n')
            ret_l = []
            for i in _read_line:
                contents = i.split(':')
                d[contents[0].strip()] = contents[1].strip()
                ret_l.append(contents[0].strip())
            ret_l = list(set(ret_l))
            ret_l.sort()
            return ret_l
        except:
            msg = traceback.format_exc()
            log_print(msg)
            return []

    def init_combobox(self):
        self.targetComboBox.clear()
        self.sourceComboBox.clear()
        targetDic.clear()
        sourceDic.clear()
        target = 'google.target.rst'
        source = 'google.source.rst'
        customEngineDic = dict()
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            customEngineDic = json.load(f)
            f.close()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                if loaded_data['engine'] in engineDic:
                    target = engineDic[loaded_data['engine']]['target']
                    source = engineDic[loaded_data['engine']]['source']
                elif loaded_data['engine'] in customEngineDic:
                    target = customEngineDic[loaded_data['engine']]['target']
                    source = customEngineDic[loaded_data['engine']]['source']
                else:
                    log_print(loaded_data['engine'] + 'not in dic')
            if target is None or source is None:
                log_print('target or source not found!')
                return
            if len(target) == 0 or len(source) == 0:
                log_print('target or source is empty!')
                return
        target = language_header + target
        source = language_header + source
        target_l = self.get_combobox_content(target, targetDic)
        for i in target_l:
            self.targetComboBox.addItem(i)
        source_l = self.get_combobox_content(source, sourceDic)
        for i in source_l:
            self.sourceComboBox.addItem(i)
        if self.localGlossaryCheckBox.isChecked():
            index = self.sourceComboBox.findText('Auto Detect')
            if index != -1:
                self.sourceComboBox.removeItem(index)
        try:
            self.sourceComboBox.setCurrentIndex(source_l.index('Auto Detect'))
        except Exception:
            pass

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('OneKeyTranslateDialog',
                                                                                'select the game file',
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
                        qDic[self.runtime_extract] = True
                        self.setEnabled(True)
            if self.path is not None:
                dir = os.path.dirname(self.path)
                target = dir + finish_flag
                if not os.path.isfile(target):
                    bat = dir + '/UnRen-forall.bat'
                    command = 'start "" /d "' + dir + '"  "' + bat + '"'
                    os.system(command)
                    while (True):
                        time.sleep(0.1)
                        if os.path.isfile(dir + '/unren.finish'):
                            os.remove(dir + '/unren.finish')
                            break
                    qDic[self.unpack] = True
                    self.clean()
                    self.path = None
                    self.setEnabled(True)
                    self.parent.showNormal()
                    self.parent.raise_()

            if self.official_extract_thread is not None:
                if not self.official_extract_thread.is_alive():
                    self.official_extract_thread = None
                    qDic[self.official_extract] = True
                    self.setEnabled(True)

            if not q.empty():
                if self.parent.isHidden():
                    self.parent.showNormal()
                    self.parent.raise_()
                if not self.isHidden():
                    self.hide()
                func = q.peek()
                if not qDic[func]:
                    if self.isEnabled():
                        func()
                else:
                    q.get()
            else:
                if self.isHidden() and self.parent.widget.isHidden():
                    if self.parent.editor_form is not None and not self.parent.editor_form.isHidden():
                        pass
                    else:
                        self.show()
                        self.raise_()
                        msg_box = QMessageBox()
                        msg_box.setWindowTitle('o(≧口≦)o')
                        msg_box.setText(
                            QCoreApplication.translate('OneKeyTranslateDialog', 'One Key Translate Complete', None))
                        msg_box.exec()
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
