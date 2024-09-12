import _thread
import io
import json
import os
import queue
import shutil
import subprocess
import time
import traceback
import webbrowser

import win32gui
from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from one_key_translate import Ui_OneKeyTranslateDialog
from custom_engine_form import sourceDic, targetDic
from my_log import log_print
from renpy_translate import engineDic, language_header, translateThread, translate_threads, get_translated_dic, \
    web_brower_export_name, rpy_info_dic, get_rpy_info, web_brower_translate, engineList
from engine_form import MyEngineForm
from game_unpacker_form import finish_flag
from extract_runtime_form import extract_finish
import extract_runtime_form
import renpy_extract
from renpy_fonts import GenGuiFonts
import game_unpacker_form
import add_change_language_entrance_form
from extraction_official_form import exec_official_translate
import extraction_official_form
from font_util import get_default_font_path
import my_log
from font_replace_form import replaceFontThread
import default_language_form
from error_repair_form import repairThread
from translated_form import MyTranslatedForm


class MyQueue(queue.Queue):
    def peek(self):
        """Return the first element in the queue without removing it."""
        with self.mutex:
            return self.queue[0]


class MyOneKeyTranslateForm(QDialog, Ui_OneKeyTranslateDialog):
    def __init__(self, parent=None):
        super(MyOneKeyTranslateForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('main.ico'))
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.init_combobox()
        self.tlNameText.textChanged.connect(self.on_tl_path_changed)
        self.changeTranslationEngineButton.clicked.connect(self.show_engine_settings)
        self.filterLengthLineEdit.setValidator(QIntValidator(1, 99, self))
        self.filterLengthLineEdit_2.setValidator(QIntValidator(1, 99, self))
        self.maxRecursionLineEdit.setValidator(QIntValidator(1, 65535, self))
        self.maxRecursionLineEdit.setText('32')
        self.local_glossary = None
        self.localGlossaryCheckBox.clicked.connect(self.on_local_glossary_checkbox_state_changed)
        self.selectFontBtn.clicked.connect(self.select_font)
        self.startButton.clicked.connect(self.on_start_button_clicked)
        self.path = None
        self.official_extract_thread = None
        self.repair_thread = None
        self.replace_font_thread = None
        self.is_queue_task_empty = True
        self.q = MyQueue()
        # a dict records the task status
        # is_finished
        # is_executed
        self.qDic = dict()
        self.dir = None
        self.select_dir = None
        default_font = get_default_font_path()
        if default_font is not None:
            self.selectFontText.setText(default_font)
        f = io.open(game_unpacker_form.hook_script, mode='r', encoding='utf-8')
        _read_lines = f.readlines()
        f.close()
        max_thread_num = 12
        is_script_only = True
        is_skip_if_exist = True
        for idx, _line in enumerate(_read_lines):
            if _line.startswith('    MAX_UNPACK_THREADS = '):
                max_thread_num = _line[len('    MAX_UNPACK_THREADS = '):].strip().strip('\n')
                break
        for idx, _line in enumerate(_read_lines):
            if _line.startswith('    SCRIPT_ONLY = '):
                is_script_only = _line[len('    SCRIPT_ONLY = '):].strip().strip('\n') == 'True'
                break
        for idx, _line in enumerate(_read_lines):
            if _line.startswith('    SKIP_IF_EXIST = '):
                is_skip_if_exist = _line[len('    SKIP_IF_EXIST = '):].strip().strip('\n') == 'True'
                break
        self.maxThreadsLineEdit.setText(str(max_thread_num))

        self.unpackAllCheckBox.setChecked(not is_script_only)
        self.overwriteCheckBox.setChecked(not is_skip_if_exist)
        _thread.start_new_thread(self.update, ())

    def on_tl_path_changed(self):
        if os.path.isfile('engine.txt'):
            json_file = open('engine.txt', 'r',encoding='utf-8')
            ori = json.load(json_file)
            json_file.close()
            ori['tl'] = self.tlNameText.toPlainText()
            json_file = open('engine.txt', 'w', encoding='utf-8')
            json.dump(ori, json_file)

    def on_start_button_clicked(self):
        self.q = MyQueue()
        self.qDic = dict()
        if self.unpackCheckBox.isChecked():
            self.q.put(self.unpack)
            self.qDic[self.unpack] = (False, False)
        if self.runtimeExtractionCheckBox.isChecked():
            self.q.put(self.runtime_extract)
            self.qDic[self.runtime_extract] = (False, False)
        if self.officialExtractionCheckBox.isChecked():
            self.q.put(self.official_extract)
            self.qDic[self.official_extract] = (False, False)
        if self.extractionCheckBox.isChecked():
            self.q.put(self.extract)
            self.qDic[self.extract] = (False, False)
        if self.replaceFontCheckBox.isChecked():
            self.q.put(self.replaceFont)
            self.qDic[self.replaceFont] = (False, False)
        if self.addEntranceCheckBox.isChecked():
            self.q.put(self.add_entrance)
            self.qDic[self.add_entrance] = (False, False)
        if self.setDefaultLanguageCheckBox.isChecked():
            self.q.put(self.set_default_language)
            self.qDic[self.set_default_language] = (False, False)
        if self.translateCheckBox.isChecked():
            self.q.put(self.translate)
            self.qDic[self.translate] = (False, False)
        if self.errorRepairCheckBox.isChecked():
            self.q.put(self.repair)
            self.qDic[self.repair] = (False, False)
        if len(self.qDic) > 0:
            self.hide()
            self.parent.showNormal()
            self.parent.raise_()

    def repair(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                t = repairThread(path, int(self.maxRecursionLineEdit.text()))
                self.repair_thread = t
                t.start()
                self.setDisabled(True)

    def set_default_language(self):
        tl_name = self.tlNameText.toPlainText()
        target = self.get_set_default_language_target()
        default_language_form.set_default_language_at_startup(tl_name, target)
        is_finished, is_executed = self.qDic[self.set_default_language]
        is_finished = True
        self.qDic[self.set_default_language] = is_finished, is_executed

    def get_set_default_language_target(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                target = os.path.dirname(path)
                target = target + '/game'
                if os.path.isdir(target):
                    target = target + '/' + default_language_form.out_default_lanugage_script_name
                    return target
        return None


    def official_extract(self):
        select_file = self.selectFileText.toPlainText()
        if len(select_file) > 0:
            select_file = select_file.replace('file:///', '')
            tl_name = self.tlNameText.toPlainText()
            if len(tl_name) == 0:
                log_print('tl_name should not be empty!')
                is_finished, is_executed = self.qDic[self.official_extract]
                is_finished = True
                self.qDic[self.official_extract] = is_finished, is_executed
                return
            if os.path.isfile(select_file):
                if select_file.endswith('.exe'):
                    t = extraction_official_form.extractThread(select_file, tl_name, False, False)
                    self.official_extract_thread = t
                    t.start()
                    self.setDisabled(True)

    def translate(self):
        if os.path.isfile(web_brower_export_name):
            os.remove(web_brower_export_name)
        select_file = self.selectFileText.toPlainText()
        if len(select_file) > 0:
            select_file = select_file.replace('file:///', '')
            tl_name = self.tlNameText.toPlainText()
            if len(tl_name) == 0:
                log_print('tl_name should not be empty!')
                is_finished, is_executed = self.qDic[self.translate]
                is_finished = True
                self.qDic[self.translate] = is_finished, is_executed
                return
            select_dir = os.path.dirname(select_file) + '/game/tl/' + tl_name
            self.select_dir = select_dir
            if not os.path.exists(select_dir):
                log_print(select_dir + ' directory does not exist!')
                is_finished, is_executed = self.qDic[self.translate]
                is_finished = True
                self.qDic[self.translate] = is_finished, is_executed
            else:
                if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                    select_dir = select_dir + '/'
                paths = os.walk(select_dir, topdown=False)
                cnt = 0
                target_language = ''
                source_language = ''
                if self.targetComboBox.currentText() != '':
                    target_language = targetDic[self.targetComboBox.currentText()]
                if self.sourceComboBox.currentText() != '':
                    source_language = sourceDic[self.sourceComboBox.currentText()]
                for path, dir_lst, file_lst in paths:
                    for file_name in file_lst:
                        i = os.path.join(path, file_name)
                        if not file_name.endswith("rpy"):
                            continue
                        t = translateThread(cnt, i, target_language, source_language,
                                            True,
                                            False, self.local_glossary, True,
                                            True, self.filterCheckBox_2.isChecked(), self.filterLengthLineEdit_2.text(), True)
                        translate_threads.append(t)
                        cnt = cnt + 1
                if len(translate_threads) > 0:
                    is_finished, is_executed = self.qDic[self.translate]
                    is_finished = False
                    self.qDic[self.translate] = is_finished, is_executed
                    log_print('start translate...')
                    for t in translate_threads:
                        t.start()
                    self.setDisabled(True)
                    _thread.start_new_thread(self.translate_threads_over, ())
                else:
                    is_finished, is_executed = self.qDic[self.translate]
                    is_finished = True
                    self.qDic[self.translate] = is_finished, is_executed
        else:
            is_finished, is_executed = self.qDic[self.translate]
            is_finished = True
            self.qDic[self.translate] = is_finished, is_executed

    def translate_threads_over(self):
        while True:
            threads_len = len(translate_threads)
            if threads_len > 0:
                for t in translate_threads:
                    if t.is_alive():
                        t.join()
                    translate_threads.remove(t)
            else:
                break
        log_print('translate all complete!')
        is_finished, is_executed = self.qDic[self.translate]
        is_finished = True
        self.qDic[self.translate] = is_finished, is_executed

    def add_entrance(self):
        target = self.get_add_entrance_target()
        if target is not None:
            log_print('start add entrance...')
            shutil.copyfile(add_change_language_entrance_form.hook_script, target)
            log_print('add entrance complete!')
        is_finished, is_executed = self.qDic[self.add_entrance]
        is_finished = True
        self.qDic[self.add_entrance] = is_finished, is_executed

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
                is_finished, is_executed = self.qDic[self.replaceFont]
                is_finished = True
                self.qDic[self.replaceFont] = is_finished, is_executed
                return
            select_dir = os.path.dirname(select_file) + '/game/tl/' + tl_name
            if not os.path.exists(select_dir):
                log_print(select_dir + ' directory does not exist!')
            else:
                if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                    select_dir = select_dir + '/'
                font_path = self.selectFontText.toPlainText()
                font_path = font_path.replace('file:///', '')
                t = replaceFontThread(select_dir, font_path, self.rtlCheckBox.isChecked())
                self.replace_font_thread = t
                t.start()
                self.setDisabled(True)
                is_finished, is_executed = self.qDic[self.replaceFont]
                is_finished = False
                self.qDic[self.replaceFont] = is_finished, is_executed
                return
        is_finished, is_executed = self.qDic[self.replaceFont]
        is_finished = True
        self.qDic[self.replaceFont] = is_finished, is_executed

    def extract(self):
        # noinspection PyBroadException
        try:
            select_file = self.selectFileText.toPlainText()
            if len(select_file) > 0:
                select_file = select_file.replace('file:///', '')
                tl_name = self.tlNameText.toPlainText()
                if len(tl_name) == 0:
                    log_print('tl_name should not be empty!')
                    is_finished, is_executed = self.qDic[self.extract]
                    is_finished = True
                    self.qDic[self.extract] = is_finished, is_executed
                    return
                select_dir = os.path.dirname(select_file) + '/game/tl/' + tl_name
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    t = renpy_extract.extractThread(threadID=0, p=None, tl_name=tl_name, dirs=None, tl_dir=select_dir,
                                                    is_open_filter=self.filterCheckBox.isChecked(),
                                                    filter_length=int(self.filterLengthLineEdit.text()),
                                                    is_gen_empty=False, is_skip_underline=self.underlineCheckBox.isChecked())
                    renpy_extract.extract_threads.append(t)

            if len(renpy_extract.extract_threads) > 0:
                is_finished, is_executed = self.qDic[self.extract]
                is_finished = False
                self.qDic[self.extract] = is_finished, is_executed
                log_print('start extract...')
                for t in renpy_extract.extract_threads:
                    t.start()
                self.setDisabled(True)
                _thread.start_new_thread(self.extract_threads_over, ())
            else:
                is_finished, is_executed = self.qDic[self.extract]
                is_finished = True
                self.qDic[self.extract] = is_finished, is_executed
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            is_finished, is_executed = self.qDic[self.extract]
            is_finished = True
            self.qDic[self.extract] = is_finished, is_executed

    def extract_threads_over(self):
        while True:
            threads_len = len(renpy_extract.extract_threads)
            if threads_len > 0:
                for t in renpy_extract.extract_threads:
                    if t.is_alive():
                        t.join()
                    renpy_extract.extract_threads.remove(t)
                else:
                    break
        log_print('extract all complete!')
        is_finished, is_executed = self.qDic[self.extract]
        is_finished = True
        self.qDic[self.extract] = is_finished, is_executed

    def runtime_extract(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        tl_name = self.tlNameText.toPlainText().strip('\n').strip()
        if len(tl_name) == 0:
            log_print('tl_name should not be empty')
            is_finished, is_executed = self.qDic[self.runtime_extract]
            is_finished = True
            self.qDic[self.runtime_extract] = is_finished, is_executed
            return
        if os.path.isfile(path):
            if path.endswith('.exe'):
                is_finished, is_executed = self.qDic[self.runtime_extract]
                is_finished = False
                self.qDic[self.runtime_extract] = is_finished, is_executed
                log_print('start runtime extract...')
                t = extract_runtime_form.extractThread(path, tl_name, False, False)
                t.start()
                self.setDisabled(True)
                return
        is_finished, is_executed = self.qDic[self.runtime_extract]
        is_finished = True
        self.qDic[self.runtime_extract] = is_finished, is_executed

    def closeEvent(self, event):
        self.parent.widget.show()
        self.parent.menubar.show()
        self.parent.versionLabel.show()
        self.parent.actionone_key_translate.triggered.connect(lambda: self.parent.show_one_key_translate_form())
        self.parent.init_combobox()
        self.parent.showNormal()
        self.hide()
        event.ignore()
        return

    def unpack(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                #shutil.copyfile(game_unpacker_form.hook_script, dir + '/game/' + game_unpacker_form.hook_script)
                f = io.open(game_unpacker_form.hook_script, mode='r', encoding='utf-8')
                _read_lines = f.readlines()
                f.close()
                for idx, _line in enumerate(_read_lines):
                    if _line.startswith('    MAX_UNPACK_THREADS = '):
                        _read_lines[idx] = f'    MAX_UNPACK_THREADS = {self.maxThreadsLineEdit.text()}\n'
                        break
                for idx, _line in enumerate(_read_lines):
                    if _line.startswith('    SCRIPT_ONLY = '):
                        _read_lines[idx] = f'    SCRIPT_ONLY = {str(not self.unpackAllCheckBox.isChecked())}\n'
                        break
                for idx, _line in enumerate(_read_lines):
                    if _line.startswith('    SKIP_IF_EXIST = '):
                        _read_lines[idx] = f'    SKIP_IF_EXIST = {str(not self.overwriteCheckBox.isChecked())}\n'
                        break
                f = io.open(dir + '/game/' + game_unpacker_form.hook_script, mode='w', encoding='utf-8')
                f.writelines(_read_lines)
                f.close()
                f = io.open(game_unpacker_form.hook_script, mode='w', encoding='utf-8')
                f.writelines(_read_lines)
                f.close()
                command = '"' +path+'"'
                self.path = path
                f = io.open(dir + finish_flag, 'w')
                f.write('waiting')
                f.close()
                self.setDisabled(True)
                log_print('start unpacking...')
                p = subprocess.Popen(command, shell=True, stdout=my_log.f, stderr=my_log.f,
                                     creationflags=0x08000000, text=True, cwd=dir, encoding='utf-8')
                return
        is_finished, is_executed = self.qDic[self.unpack]
        is_finished = True
        self.qDic[self.unpack] = is_finished, is_executed

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
            if len(_read) == 0:
                return []
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

    def on_combobox_changed(self):
        if os.path.isfile('engine.txt'):
            json_file = open('engine.txt', 'r',encoding='utf-8')
            ori = json.load(json_file)
            json_file.close()
            current_engine = ori['engine']
            dic = dict()
            dic['target'] = self.targetComboBox.currentText()
            dic['source'] = self.sourceComboBox.currentText()
            ori[current_engine] = dic
            json_file = open('engine.txt', 'w', encoding='utf-8')
            json.dump(ori, json_file)

    def init_combobox(self):
        self.targetComboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.sourceComboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.targetComboBox.currentTextChanged.disconnect()
        self.sourceComboBox.currentTextChanged.disconnect()
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
        if os.path.isfile('engine.txt'):
            json_file = open('engine.txt', 'r', encoding='utf-8')
            json_data = json.load(json_file)
            json_file.close()
            current_engine = json_data['engine']
            if 'tl' in json_data:
                self.tlNameText.setPlainText(json_data['tl'])
            if current_engine in json_data:
                combobox_data = json_data[current_engine]
                if 'source' in combobox_data:
                    try:
                        self.sourceComboBox.setCurrentIndex(source_l.index(combobox_data['source']))
                    except:
                        pass
                if 'target' in combobox_data:
                    try:
                        self.targetComboBox.setCurrentIndex(target_l.index(combobox_data['target']))
                    except:
                        pass
        self.targetComboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.sourceComboBox.currentTextChanged.connect(self.on_combobox_changed)

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
            if self.dir is not None:
                if os.path.isfile(self.dir + '/unren.finish'):
                    os.remove(self.dir + '/unren.finish')
                    self.dir = None
                    is_finished, is_executed = self.qDic[self.unpack]
                    is_finished = True
                    self.qDic[self.unpack] = is_finished, is_executed
                    self.path = None
                    log_print('unpack complete!')
            if self.runtime_extract in self.qDic:
                if os.path.isfile(extract_finish):
                    os.remove(extract_finish)
                    if not os.path.isfile(extract_finish):
                        is_finished, is_executed = self.qDic[self.runtime_extract]
                        is_finished = True
                        self.qDic[self.runtime_extract] = is_finished, is_executed
            if self.path is not None:
                dir = os.path.dirname(self.path)
                target = dir + finish_flag
                if not os.path.isfile(target):
                    hook_script_path = dir + '/game/' + game_unpacker_form.hook_script
                    if os.path.isfile(hook_script_path):
                        os.remove(hook_script_path)
                    if os.path.isfile(hook_script_path + 'c'):
                        os.remove(hook_script_path + 'c')
                    pid = None
                    target = dir + game_unpacker_form.pid_flag
                    if os.path.isfile(target):
                        f = io.open(target, 'r', encoding='utf-8')
                        pid = f.read()
                        f.close()
                        os.remove(target)
                    t = game_unpacker_form.unrpycThread(dir, self.path, pid, self.overwriteCheckBox.isChecked(), True)
                    t.start()
                    self.path = None
                    self.dir = dir

            if self.official_extract_thread is not None:
                if not self.official_extract_thread.is_alive():
                    self.official_extract_thread = None
                    is_finished, is_executed = self.qDic[self.official_extract]
                    is_finished = True
                    self.qDic[self.official_extract] = is_finished, is_executed

            if self.repair_thread is not None:
                if not self.repair_thread.is_alive():
                    self.repair_thread = None
                    is_finished, is_executed = self.qDic[self.repair]
                    is_finished = True
                    self.qDic[self.repair] = is_finished, is_executed

            if self.replace_font_thread is not None:
                if not self.replace_font_thread.is_alive():
                    self.replace_font_thread = None
                    is_finished, is_executed = self.qDic[self.replaceFont]
                    is_finished = True
                    self.qDic[self.replaceFont] = is_finished, is_executed

            if not self.q.empty():
                self.is_queue_task_empty = False
                func = self.q.peek()
                # the task is not finished and executed
                if not self.qDic[func][0]:
                    if not self.qDic[func][1]:
                        func()
                        is_finished, is_executed = self.qDic[func]
                        is_executed = True
                        self.qDic[func] = is_finished, is_executed
                else:
                    self.q.get()
                    self.qDic.pop(func, None)
                    if func == self.translate:
                        global rpy_info_dic
                        if os.path.isfile('engine.txt'):
                            with open('engine.txt', 'r', encoding='utf-8') as json_file:
                                loaded_data = json.load(json_file)
                                if loaded_data['engine'] == engineList[12]:
                                    if os.path.isfile(web_brower_export_name):
                                        webbrowser.open(web_brower_export_name)
                                        translated_form = MyTranslatedForm()
                                        translated_form.exec()
                                        f = io.open('translated.txt', 'w', encoding='utf-8')
                                        f.write(translated_form.plainTextEdit.toPlainText())
                                        f.close()
                                        dic, is_replace_special_symbols = get_translated_dic(web_brower_export_name, 'translated.txt')
                                        if dic is None:
                                            msg_box = QMessageBox()
                                            msg_box.setWindowTitle('o(≧口≦)o')
                                            msg_box.setText(
                                                QCoreApplication.translate('ImportHtmlDialog',
                                                                           'The html file does not match the translated file , please check the input files',
                                                                           None))
                                            msg_box.exec()
                                            rpy_info_dic.clear()
                                        else:
                                            if self.select_dir is not None and os.path.isdir(self.select_dir):
                                                paths = os.walk(self.select_dir, topdown=False)
                                                for path, dir_lst, file_lst in paths:
                                                    for file_name in file_lst:
                                                        i = path + '/' + file_name
                                                        if not file_name.endswith("rpy"):
                                                            continue
                                                        if i in rpy_info_dic.keys():
                                                            ret, unmatch_cnt, p = rpy_info_dic[i]
                                                        else:
                                                            ret, unmatch_cnt, p = get_rpy_info(i)
                                                            rpy_info_dic[i] = ret, unmatch_cnt, p
                                                        web_brower_translate(self.filterCheckBox.isChecked(),
                                                                             self.filterLengthLineEdit.text(), True,
                                                                             is_replace_special_symbols, i, ret, dic)
                                        rpy_info_dic.clear()
                                        if os.path.isfile(web_brower_export_name):
                                            os.remove(web_brower_export_name)
                                    else:
                                        log_print('nothing to translate')
            else:
                if not self.is_queue_task_empty:
                    if len(rpy_info_dic) == 0:
                        self.is_queue_task_empty = True
                        self.show()
                        self.raise_()
                        msg_box = QMessageBox(parent=self)
                        msg_box.setWindowTitle('o(≧口≦)o')
                        msg_box.setText(
                            QCoreApplication.translate('OneKeyTranslateDialog', 'One Key Translate Complete', None))
                        msg_box.exec()
                        self.setEnabled(True)
                        self.qDic.clear()

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
