import _thread
import io
import json
import os.path
import shutil
import sys
import time
import traceback
import webbrowser

from PySide6 import QtCore
from PySide6.QtCore import QThread, Signal, QCoreApplication
from PySide6.QtGui import QTextCursor, Qt
from PySide6.QtWidgets import QDialog, QFileDialog

from custom_engine import Ui_CustomDialog
from custom_translate import CustomTranslate
from my_log import log_path, log_print, MAX_LOG_LINES
from renpy_translate import language_header, custom_header
from string_tool import tail

targetDic = dict()
sourceDic = dict()

class MyCustomEngineForm(QDialog, Ui_CustomDialog):
    def __init__(self, parent=None):
        super(MyCustomEngineForm, self).__init__(parent)
        self.setupUi(self)
        self.detailLabel.setStyleSheet(
            "QLabel::hover"
            "{"
            "background-color : lightgreen;"
            "}"
        )
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        _thread.start_new_thread(self.update_log, ())
        self.nameLineEdit.textChanged.connect(self.refresh_name)
        self.urlLineEdit.textChanged.connect(self.refresh_url)
        self.detailLabel.mousePressEvent = self.open_url
        self.detailLabel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.keyCheckBox.setChecked(True)
        self.secretCheckBox.setChecked(False)
        self.refresh_key_secret_edit()
        self.keyCheckBox.stateChanged.connect(self.refresh_key_secret_edit)
        self.secretCheckBox.stateChanged.connect(self.refresh_key_secret_edit)
        self.renameScriptCheckBox.stateChanged.connect(self.refresh_rename_checkbox)
        self.renameSourceCheckBox.stateChanged.connect(self.refresh_rename_checkbox)
        self.renameTargetCheckBox.stateChanged.connect(self.refresh_rename_checkbox)
        self.refresh_rename_checkbox()

        self.selectSourceText.textChanged.connect(self.refresh_source_target)
        self.selectTargetText.textChanged.connect(self.refresh_source_target)
        self.refresh_source_target()
        self.clearLogBtn.clicked.connect(self.clear_log)
        self.testButton.clicked.connect(self.on_test_button_clicked)
        self.selectScriptBtn.clicked.connect(self.select_script_file)
        self.selectSourceBtn.clicked.connect(self.select_source_file)
        self.selectTargetBtn.clicked.connect(self.select_target_file)
        self.saveButton.clicked.connect(self.on_save_button_clicked)
        self.deleteButton.clicked.connect(self.on_delete_button_clicked)
        self.customComboBox.currentIndexChanged.connect(self.refresh_custom)
        self.init_key_secret()
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            loaded_data = json.load(f)
            f.close()
            for i in loaded_data.keys():
                self.customComboBox.addItem(i)

    def init_key_secret(self):
        self.keyEdit.setText('')
        self.secretEdit.setText('')
        if os.path.isfile('engine.txt'):
            f = io.open('engine.txt', 'r', encoding='utf-8')
            loaded_data = json.load(f)
            f.close()
            key = self.customComboBox.currentText() + '_key'
            secret = self.customComboBox.currentText() + '_secret'
            if key in loaded_data.keys():
                self.keyEdit.setText(loaded_data[key])
            else:
                self.keyEdit.setText('')
            if secret in loaded_data.keys():
                self.secretEdit.setText(loaded_data[secret])
            else:
                self.secretEdit.setText('')


    def on_delete_button_clicked(self):
        if self.customComboBox.currentIndex()==0 or not os.path.isfile('custom.txt'):
            return
        f = io.open('custom.txt', 'r', encoding='utf-8')
        dic = json.load(f)
        f.close()
        if self.customComboBox.currentText() not in dic.keys():
            return
        del dic[self.customComboBox.currentText()]
        self.customComboBox.setCurrentIndex(0)
        f = io.open('custom.txt', 'w', encoding='utf-8')
        json.dump(dic, f)
        f.close()
        self.customComboBox.clear()
        self.customComboBox.addItem(QCoreApplication.translate("CustomDialog", u"add a new custom engine", None))
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            loaded_data = json.load(f)
            f.close()
            for i in loaded_data.keys():
                self.customComboBox.addItem(i)

    def refresh_custom(self):
        if self.customComboBox.currentIndex() == 0:
            self.nameLineEdit.setText('')
            self.urlLineEdit.setText('')
            self.keyCheckBox.setChecked(True)
            self.secretCheckBox.setChecked(False)
            self.queueCheckBox.setChecked(False)
            self.selectScriptText.setText('')
            self.selectTargetText.setText('')
            self.selectSourceText.setText('')
        else:
            f = io.open('custom.txt', 'r', encoding='utf-8')
            dic = json.load(f)
            f.close()
            if self.customComboBox.currentText() in dic:
                sub_dic = dic[self.customComboBox.currentText()]
                self.nameLineEdit.setText(self.customComboBox.currentText())
                self.urlLineEdit.setText(sub_dic['url'])
                self.keyCheckBox.setChecked(sub_dic['key_edit'])
                self.secretCheckBox.setChecked(sub_dic['secret_edit'])
                self.queueCheckBox.setChecked(sub_dic['is_queue'])
                self.selectScriptText.setText(os.getcwd()+'/'+ custom_header+sub_dic['file_name'])
                self.selectTargetText.setText(os.getcwd()+'/'+language_header+sub_dic['target'])
                self.selectSourceText.setText(os.getcwd()+'/'+language_header+sub_dic['source'])
            else:
                self.nameLineEdit.setText('')
                self.urlLineEdit.setText('')
                self.keyCheckBox.setChecked(True)
                self.secretCheckBox.setChecked(False)
                self.queueCheckBox.setChecked(False)
                self.selectScriptText.setText('')
                self.selectTargetText.setText('')
                self.selectSourceText.setText('')
        self.init_key_secret()
    def on_save_button_clicked(self):
        dic = dict()
        name = self.nameLineEdit.text()
        if not os.path.isfile('custom.txt'):
            dic[name] = dict()
        else:
            f = io.open('custom.txt', 'r', encoding='utf-8')
            dic = json.load(f)
            f.close()
            if name not in dic:
                dic[name] = dict()
        sub_dic = dic[name]
        sub_dic['url'] = self.urlLineEdit.text()
        sub_dic['key_edit'] = self.keyCheckBox.isChecked()
        sub_dic['secret_edit'] = self.secretCheckBox.isChecked()
        sub_dic['is_queue'] = self.queueCheckBox.isChecked()
        cur_file_name = self.selectScriptText.toPlainText().replace('file:///', '')
        file_name = os.path.basename(cur_file_name)
        if self.renameScriptCheckBox.isChecked():
            file_name = self.renameScriptLineEdit.text()
        cur_target = self.selectTargetText.toPlainText().replace('file:///', '')
        target = os.path.basename(cur_target)
        if self.renameTargetCheckBox.isChecked():
            target = self.renameTargetLineEdit.text()
        cur_source = self.selectSourceText.toPlainText().replace('file:///', '')
        source = os.path.basename(cur_source)
        if self.renameSourceCheckBox.isChecked():
            source = self.renameSourceLineEdit.text()
        sub_dic['target'] = target
        sub_dic['source'] = source
        sub_dic['file_name'] = file_name
        f = io.open('custom.txt', 'w', encoding='utf-8')
        json.dump(dic, f)
        f.close()
        if self.saveKeySecretCheckBox.isChecked():
            key = name + '_key'
            secret = name + '_secret'
            if os.path.isfile('engine.txt'):
                f = io.open('engine.txt', 'r', encoding='utf-8')
                loaded_data = json.load(f)
                f.close()
                loaded_data[key] = self.keyEdit.text()
                loaded_data[secret] = self.secretEdit.text()
                if loaded_data['engine'] == self.customComboBox.currentText():
                    loaded_data['key'] = loaded_data[key]
                    loaded_data['secret'] = loaded_data[secret]
                f = io.open('engine.txt', 'w', encoding='utf-8')
                json.dump(loaded_data, f)
                f.close()
            else:
                f = io.open('engine.txt', 'w', encoding='utf-8')
                loaded_data = {key:self.keyEdit.text(),secret:self.secretEdit.text(),'engine':name,'key':self.keyEdit.text(),'secret':self.secretEdit.text()}
                json.dump(loaded_data, f)
                f.close()
        self.customComboBox.clear()
        self.customComboBox.addItem(QCoreApplication.translate("CustomDialog", u"add a new custom engine", None))
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            loaded_data = json.load(f)
            f.close()
            cur_i = 0
            for i,e in enumerate(loaded_data.keys()):
                self.customComboBox.addItem(e)
                if e == name:
                    cur_i = i+1
            self.customComboBox.setCurrentIndex(cur_i)
        try:
            shutil.copy(cur_file_name, custom_header + file_name)
        except Exception:
            pass
        try:
            shutil.copy(cur_source,language_header + source)
        except Exception:
            pass
        try:
            shutil.copy(cur_target,language_header + target)
        except Exception:
            pass

    def on_test_button_clicked(self):
        proxies = None
        if os.path.isfile('proxy.txt'):
            with open('proxy.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                if loaded_data['enable']:
                    proxies = {'https': loaded_data['proxy']}
                    os.environ['HTTPS_PROXY'] = loaded_data['proxy']
                    os.environ['HTTP_PROXY'] = loaded_data['proxy']
                    if 'NO_PROXY' in os.environ.keys():
                        del os.environ['NO_PROXY']
                else:
                    if 'HTTPS_PROXY' in os.environ.keys():
                        del os.environ['HTTPS_PROXY']
                    if 'HTTP_PROXY' in os.environ.keys():
                        del os.environ['HTTP_PROXY']
                    os.environ['NO_PROXY'] = '*'
        app_key = self.keyEdit.text()
        if not self.keyCheckBox.isChecked():
            app_key = None
        app_secret = self.secretEdit.text()
        if not self.secretCheckBox.isChecked():
            app_secret = None

        file_name = self.selectScriptText.toPlainText()
        if len(file_name) > 0:
            file_name = file_name.replace('file:///', '')
        else:
            log_print('script empty!')
            return
        if not os.path.isfile(file_name):
            log_print('script not exist!')
            return
        if sourceDic is None or targetDic is None or self.sourceComboBox.currentText() not in sourceDic or self.targetComboBox.currentText() not in targetDic:
            log_print('source or target not correct')
            return

        customTranslate = CustomTranslate(file_name,app_key,app_secret,proxies,self.queueCheckBox.isChecked())
        result = customTranslate.translate([self.untranslatedEdit.text(),self.untranslatedEdit.text()],sourceDic[self.sourceComboBox.currentText()],targetDic[self.targetComboBox.currentText()])
        for i in result:
            log_print(i.untranslatedText+' : '+i.translatedText)

    def select_target_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                       "select the supported language file",
                                                       '',
                                                       "RST Files (*.rst);;All Files (*)")
        if file is not None and len(file) > 0:
            self.selectTargetText.setText(file)

    def select_source_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                       "select the supported language file",
                                                       '',
                                                       "RST Files (*.rst);;All Files (*)")
        if file is not None and len(file) > 0:
            self.selectSourceText.setText(file)

    def select_script_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                       "select the script file",
                                                       '',
                                                       "Python Files (*.py);;All Files (*)")
        if file is not None and len(file) > 0:
            self.selectScriptText.setText(file)

    @staticmethod
    def clear_log():
        f = io.open(log_path, 'w', encoding='utf-8')
        f.write('')
        f.close()

    def update_log(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(1)

    def update_progress(self, data):
        if data != self.logTextEdit.toPlainText():
            self.logTextEdit.setText(data)
            self.logTextEdit.moveCursor(QTextCursor.End)

    class UpdateThread(QThread):
        update_date = Signal(str)

        def __init__(self):
            super().__init__()

        def __del__(self):
            self.wait()

        def run(self):
            _lines = tail(log_path, MAX_LOG_LINES)
            _data = ''
            for line in _lines:
                _data += line + '\n'
            if len(_lines) == MAX_LOG_LINES:
                _data += f'log is too large, only show last {str(MAX_LOG_LINES)} lines\n'
            self.update_date.emit(_data)

    @staticmethod
    def get_combobox_content(p, d):
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

    def refresh_source_target(self):
        self.targetComboBox.clear()
        self.sourceComboBox.clear()
        targetDic.clear()
        sourceDic.clear()
        select_source = self.selectSourceText.toPlainText()
        if len(select_source) > 0:
            select_source = select_source.replace('file:///', '')
        if os.path.isfile(select_source):
            source_l = self.get_combobox_content(select_source, sourceDic)
            for i in source_l:
                self.sourceComboBox.addItem(i)
            try:
                self.sourceComboBox.setCurrentIndex(source_l.index('Auto Detect'))
            except Exception:
                pass
        select_target = self.selectTargetText.toPlainText()
        if len(select_target) > 0:
            select_target = select_target.replace('file:///', '')
        if os.path.isfile(select_target):
            target_l = self.get_combobox_content(select_target, targetDic)
            for i in target_l:
                self.targetComboBox.addItem(i)


    def refresh_rename_checkbox(self):
        if self.renameScriptCheckBox.isChecked():
            self.renameScriptLineEdit.setEnabled(True)
        else:
            self.renameScriptLineEdit.setDisabled(True)

        if self.renameSourceCheckBox.isChecked():
            self.renameSourceLineEdit.setEnabled(True)
        else:
            self.renameSourceLineEdit.setDisabled(True)

        if self.renameTargetCheckBox.isChecked():
            self.renameTargetLineEdit.setEnabled(True)
        else:
            self.renameTargetLineEdit.setDisabled(True)

    def refresh_key_secret_edit(self):
        if self.keyCheckBox.isChecked():
            self.keyEdit.setEnabled(True)
        else:
            self.keyEdit.setDisabled(True)
        if self.secretCheckBox.isChecked():
            self.secretEdit.setEnabled(True)
        else:
            self.secretEdit.setDisabled(True)

    def refresh_url(self):
        self.url = self.urlLineEdit.text()

    def refresh_name(self):
        self.engineComboBox.clear()
        self.engineComboBox.addItem(self.nameLineEdit.text())

    def open_url(self, event):
        webbrowser.open(self.url)
