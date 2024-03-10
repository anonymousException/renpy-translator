import _thread
import io
import os.path
import subprocess
import sys
import time
import traceback
import webbrowser
import json

from PySide6 import QtWidgets, QtCore
import sys

from PySide6.QtCore import Qt, QDir, QThread, Signal
from PySide6.QtGui import QIcon, QIntValidator, QTextCursor
from PySide6.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView, QDialog, QPushButton, QLineEdit, \
    QVBoxLayout, QMainWindow, QApplication

from copyright import Ui_CopyrightDialog
from my_log import log_print, log_path
from renpy_extract import extractThread, extract_threads, ExtractAllFilesInDir
from renpy_fonts import GenGuiFonts


os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
os.environ['NO_PROXY'] = '*'
from renpy_translate import translateThread, translate_threads, engineList, engineDic, customEngineDic, language_header
from proxy import Ui_ProxyDialog
from engine import Ui_EngineDialog
from ui import Ui_MainWindow
from custom_engine_form import MyCustomEngineForm

targetDic = dict()
sourceDic = dict()

from custom_translate import CustomTranslate
# customTranslate = CustomTranslate('test.txt','3975l6lr5pcbvidl6jl2',None,{'http':'http://localhost:10809'},True)
# result = customTranslate.translate(['What are you doing'],'auto','zh')
# log_print(result)

class MyEngineForm(QDialog, Ui_EngineDialog):
    def __init__(self, parent=None):
        super(MyEngineForm, self).__init__(parent)
        self.setupUi(self)
        self.detailLabel.setStyleSheet(
            "QLabel::hover"
            "{"
            "background-color : lightgreen;"
            "}"
        )
        self.detailLabel.setStyleSheet("color:blue")
        self.setFixedHeight(200)
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            customEngineDic = json.load(f)
            f.close()
        for i in engineDic.keys():
            self.engineComboBox.addItem(i)
        for i in customEngineDic.keys():
            self.engineComboBox.addItem(i)
        self.init_openai_model_combobox()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                self.engineComboBox.setCurrentIndex(self.engineComboBox.findText(loaded_data['engine']))
                self.keyEdit.setText(loaded_data['key'])
                self.secretEdit.setText((loaded_data['secret']))
                if "rpm" in loaded_data:
                    self.rpmEdit.setText(loaded_data['rpm'])
                if "rps" in loaded_data:
                    self.rpsEdit.setText(loaded_data['rps'])
                if "tpm" in loaded_data:
                    self.tpmEdit.setText(loaded_data['tpm'])
                if "openai_model_index" in loaded_data:
                    self.modelComboBox.setCurrentIndex(loaded_data['openai_model_index'])
                if "openai_base_url" in loaded_data:
                    self.baseUrlEdit.setText(loaded_data['openai_base_url'])
            self.init_edit_status()
            if self.engineComboBox.currentText() == engineList[4]:
                self.setFixedHeight(300)
        else:
            self.engineComboBox.setCurrentIndex(0)
            self.on_combobox_change()
        self.confirmButton.clicked.connect(self.confirm)
        self.engineComboBox.currentIndexChanged.connect(self.on_combobox_change)
        self.detailLabel.mousePressEvent = self.open_url
        self.detailLabel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def init_edit_status(self):
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            customEngineDic = json.load(f)
            f.close()
        if self.engineComboBox.currentText() in engineDic.keys():
            if engineDic[self.engineComboBox.currentText()]['key_edit']:
                self.keyEdit.setEnabled(True)
            else:
                self.keyEdit.setDisabled(True)

            if engineDic[self.engineComboBox.currentText()]['secret_edit']:
                self.secretEdit.setEnabled(True)
            else:
                self.secretEdit.setDisabled(True)
        elif self.engineComboBox.currentText() in customEngineDic.keys():
            if customEngineDic[self.engineComboBox.currentText()]['key_edit']:
                self.keyEdit.setEnabled(True)
            else:
                self.keyEdit.setDisabled(True)
            if customEngineDic[self.engineComboBox.currentText()]['secret_edit']:
                self.secretEdit.setEnabled(True)
            else:
                self.secretEdit.setDisabled(True)
        else:
            log_print(self.engineComboBox.currentText() + 'not in dic error!')

    def init_openai_model_combobox(self):
        if self.modelComboBox.count() == 0:
            l = ["gpt-3.5-turbo", "gpt-4"]
            for i in l:
                self.modelComboBox.addItem(i)

    def open_url(self, event):
        webbrowser.open(engineDic[self.engineComboBox.currentText()]['url'])

    def on_combobox_change(self):
        self.setFixedHeight(200)
        if self.engineComboBox.currentText() == engineList[4]:
            self.setFixedHeight(300)
        self.init_edit_status()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                key = str(self.engineComboBox.currentText()) + '_key'
                secret = str(self.engineComboBox.currentText()) + '_secret'
                if key in loaded_data:
                    self.keyEdit.setText(loaded_data[key])
                else:
                    self.keyEdit.setText('')
                if secret in loaded_data:
                    self.secretEdit.setText(loaded_data[secret])
                else:
                    self.secretEdit.setText('')

    def confirm(self):
        if not os.path.isfile('engine.txt'):
            f = io.open('engine.txt', 'w', encoding='utf-8')
            data = {"engine": self.engineComboBox.currentText(), "key": self.keyEdit.text(),
                    "secret": self.secretEdit.text(),
                    str(self.engineComboBox.currentText()) + '_key': self.keyEdit.text(),
                    str(self.engineComboBox.currentText()) + '_secret': self.secretEdit.text(),
                    "rpm": self.rpmEdit.text(),
                    "rps": self.rpsEdit.text(),
                    "tpm": self.tpmEdit.text(),
                    "openai_model": self.modelComboBox.currentText(),
                    "openai_base_url": self.baseUrlEdit.text(),
                    "openai_model_index": self.modelComboBox.currentIndex()}
            json.dump(data, f)
            f.close()
        else:
            f = io.open('engine.txt', 'r', encoding='utf-8')
            loaded_data = json.load(f)
            f.close()
            f = io.open('engine.txt', 'w', encoding='utf-8')
            loaded_data['engine'] = self.engineComboBox.currentText()
            loaded_data['key'] = self.keyEdit.text()
            loaded_data['secret'] = self.secretEdit.text()
            loaded_data[str(self.engineComboBox.currentText()) + '_key'] = self.keyEdit.text()
            loaded_data[str(self.engineComboBox.currentText()) + '_secret'] = self.secretEdit.text()
            loaded_data['rpm'] = self.rpmEdit.text()
            loaded_data['rps'] = self.rpsEdit.text()
            loaded_data['tpm'] = self.tpmEdit.text()
            loaded_data['openai_model'] = self.modelComboBox.currentText()
            loaded_data['openai_base_url'] = self.baseUrlEdit.text()
            loaded_data['openai_model_index'] = self.modelComboBox.currentIndex()
            json.dump(loaded_data, f)
            f.close()
        self.close()


class MyProxyForm(QDialog, Ui_ProxyDialog):
    def __init__(self, parent=None):
        super(MyProxyForm, self).__init__(parent)
        self.setupUi(self)
        if os.path.isfile('proxy.txt'):
            with open('proxy.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                self.proxyEdit.setText(loaded_data['proxy'])
                self.checkBox.setChecked((loaded_data['enable']))
        self.confirmButton.clicked.connect(self.confirm)

    def confirm(self):
        f = io.open('proxy.txt', 'w', encoding='utf-8')
        data = {"proxy": self.proxyEdit.text(), "enable": self.checkBox.isChecked()}
        json.dump(data, f)
        f.close()
        self.close()


class MyCopyrightForm(QDialog, Ui_CopyrightDialog):
    def __init__(self, parent=None):
        super(MyCopyrightForm, self).__init__(parent)
        self.setupUi(self)
        self.url_label.setStyleSheet(
            "QLabel::hover"
            "{"
            "background-color : lightgreen;"
            "}"
        )
        self.url_label.setStyleSheet("color:blue")
        self.url_label.mousePressEvent = self.open_url

        self.url_label.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def open_url(self, event):
        webbrowser.open(self.url_label.text())


class DirectorySelector(QFileDialog):
    def __init__(self):
        super(DirectorySelector, self).__init__()
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        self.setDirectory(QDir.rootPath())
        listView = self.findChild(QListView, "listView")
        if listView:
            listView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        treeView = self.findChild(QTreeView, "treeView")
        if treeView:
            treeView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('main.ico'))
        self.selectFilesBtn.clicked.connect(self.select_file)
        self.selectDirBtn.clicked.connect(self.select_directory)
        self.translateBtn.clicked.connect(self.translate)
        self.clearLogBtn.clicked.connect(self.clear_log)
        self.selectFontBtn.clicked.connect(self.select_font)
        self.selectFilesBtn_2.clicked.connect(self.select_file2)
        self.selectDirBtn_2.clicked.connect(self.select_directory2)
        self.selectDirBtn_3.clicked.connect(self.select_directory3)
        self.selectDirsBtn.clicked.connect(self.select_directory4)
        self.extractBtn.clicked.connect(self.extract)
        self.replaceFontBtn.clicked.connect(self.replaceFont)
        self.openFontStyleBtn.clicked.connect(self.openFontStyleFile)
        self.multiTranslateCheckBox.setChecked(True)
        self.backupCheckBox.setChecked(True)
        self.filterCheckBox.setChecked(True)
        self.filterLengthLineEdit.setText('8')
        self.filterCheckBox.stateChanged.connect(self.filter_checkbox_changed)
        validator = QIntValidator()
        self.filterLengthLineEdit.setValidator(validator)
        try:
            self.init_combobox()
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
        self.versionLabel.setStyleSheet("color:grey")
        self.copyrightLabel.setStyleSheet("color:grey")
        self.actioncopyright.triggered.connect(lambda: self.show_copyright_form())
        self.proxySettings.triggered.connect(lambda: self.show_proxy_settings())
        self.engineSettings.triggered.connect(lambda: self.show_engine_settings())
        self.customEngineSettings.triggered.connect(lambda: self.show_custom_engine_settings())
        _thread.start_new_thread(self.update_log, ())
        if os.path.isfile('translating'):
            os.remove('translating')
        if os.path.isfile('extracting'):
            os.remove('extracting')


    def show_custom_engine_settings(self):
        custom_engine_form = MyCustomEngineForm(parent=self)
        custom_engine_form.exec()

    def filter_checkbox_changed(self, state):
        if self.filterCheckBox.isChecked():
            self.filterLengthLineEdit.setEnabled(True)
        else:
            self.filterLengthLineEdit.setDisabled(True)

    def closeEvent(self, event):
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(['taskkill.exe', '/F', '/T', '/PID', str(os.getpid())], creationflags=CREATE_NO_WINDOW)

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

    def show_proxy_settings(self):
        proxy_form = MyProxyForm(parent=self)
        proxy_form.exec()

    def replaceFont(self):
        select_dir = self.selectDirText_3.toPlainText()
        if len(select_dir) > 0:
            select_dir = select_dir.replace('file:///', '')
            if not os.path.exists(select_dir):
                log_print(select_dir + ' directory does not exist!')
            else:
                if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                    select_dir = select_dir + '/'
                font_path = self.selectFontText.toPlainText()
                font_path = font_path.replace('file:///', '')
                GenGuiFonts(select_dir, font_path)

    def openFontStyleFile(self):
        select_dir = self.selectDirText_3.toPlainText()
        if len(select_dir) > 0:
            select_dir = select_dir.replace('file:///', '')
            if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                select_dir = select_dir + '/'
            os.system('notepad ' + select_dir + 'gui.rpy')

    def show_copyright_form(self):
        copyright_form = MyCopyrightForm(parent=self)
        copyright_form.exec()

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

    def init_combobox(self):
        self.targetComboBox.clear()
        self.sourceComboBox.clear()
        target = 'google.target.rst'
        source = 'google.source.rst'
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
        try:
            self.sourceComboBox.setCurrentIndex(source_l.index('Auto Detect'))
        except Exception:
            pass

    def extract(self):
        # noinspection PyBroadException
        try:
            select_files = self.selectFilesText_2.toPlainText().split('\n')
            cnt = 0
            for i in select_files:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    tl_name = self.tlNameText.toPlainText()
                    if len(tl_name) == 0:
                        log_print('tl name is empty skip extract file(s)')
                        continue
                    t = extractThread(threadID=cnt, p=i, tl_name=tl_name, dir=None, tl_dir=None,
                                      is_open_filter=self.filterCheckBox.isChecked(),
                                      filter_length=int(self.filterLengthLineEdit.text()),
                                      is_gen_empty=self.emptyCheckBox.isChecked())
                    t.start()
                    extract_threads.append(t)
                    cnt = cnt + 1
            select_dirs = self.selectDirsText.toPlainText().split('\n')
            for i in select_dirs:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    tl_name = self.tlNameText.toPlainText()
                    if len(tl_name) == 0:
                        log_print('tl name is empty skip extract directory(s)')
                        continue
                    t = extractThread(threadID=cnt, p=None, tl_name=tl_name, dir=i, tl_dir=None,
                                      is_open_filter=self.filterCheckBox.isChecked(),
                                      filter_length=int(self.filterLengthLineEdit.text()),
                                      is_gen_empty=self.emptyCheckBox.isChecked())
                    t.start()
                    extract_threads.append(t)
                    cnt = cnt + 1
                pass

            select_dir = self.selectDirText_2.toPlainText()
            if len(select_dir) > 0:
                select_dir = select_dir.replace('file:///', '')
                tl_name = self.tlNameText.toPlainText()
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    t = extractThread(threadID=cnt, p=None, tl_name=tl_name, dir=None, tl_dir=select_dir,
                                      is_open_filter=self.filterCheckBox.isChecked(),
                                      filter_length=int(self.filterLengthLineEdit.text()),
                                      is_gen_empty=self.emptyCheckBox.isChecked())
                    t.start()
                    extract_threads.append(t)
                    cnt = cnt + 1
            if len(extract_threads) > 0:
                open('extracting', "w")
                self.extractBtn.setText('extracting...')
                self.extractBtn.setDisabled(True)
                _thread.start_new_thread(self.extract_threads_over, ())
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('extracting'):
                os.remove('extracting')

    @staticmethod
    def extract_threads_over():
        for t in extract_threads:
            t.join()
        log_print('extract all complete!')
        if os.path.isfile('extracting'):
            os.remove('extracting')

    def select_font(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     "select the file font which supports the translated language",
                                                     '',  # 起始路径
                                                     "Font Files (*.ttf || *.otf);;All Files (*)")
        self.selectFontText.setText(file)

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
        if data != self.log_text.toPlainText():
            self.log_text.setText(data)
            self.log_text.moveCursor(QTextCursor.End)
        if os.path.isfile('translating'):
            self.translateBtn.setText('translating...')
            self.translateBtn.setDisabled(True)
        else:
            self.translateBtn.setText('translate')
            self.translateBtn.setEnabled(True)

        if os.path.isfile('extracting'):
            self.extractBtn.setText('extracting...')
            self.extractBtn.setDisabled(True)
        else:
            self.extractBtn.setText('extract')
            self.extractBtn.setEnabled(True)

    class UpdateThread(QThread):
        update_date = Signal(str)

        def __init__(self):
            super().__init__()

        def __del__(self):
            self.wait()

        def run(self):
            f = io.open(log_path, 'r+', encoding='utf-8')
            self.update_date.emit(f.read())
            f.close()

    def select_directory4(self):
        directorySelector = DirectorySelector()
        if directorySelector.exec() == 1:
            folders = directorySelector.selectedFiles()
            s = ''
            for folder in folders:
                if os.path.isdir(folder):
                    s = s + folder + '\n'
            self.selectDirsText.setText(s.rstrip('\n'))

    def select_directory3(self):
        directory = QFileDialog.getExistingDirectory(self, 'select the directory you want to extract')
        self.selectDirText_3.setText(directory)

    def select_file2(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       "select the file(s) you want to extract",
                                                       '',
                                                       "Rpy Files (*.rpy);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText_2.setText(s.rstrip('\n'))

    def select_directory2(self):
        directory = QFileDialog.getExistingDirectory(self, 'select the directory you want to extract')
        self.selectDirText_2.setText(directory)

    def select_file(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       "select the file(s) you want to translate",
                                                       '',
                                                       "Rpy Files (*.rpy);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText.setText(s.rstrip('\n'))

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'select the directory you want to translate')
        self.selectDirText.setText(directory)

    def translate(self):
        # noinspection PyBroadException
        try:
            select_files = self.selectFilesText.toPlainText().split('\n')
            target_language = targetDic[self.targetComboBox.currentText()]
            source_language = sourceDic[self.sourceComboBox.currentText()]
            cnt = 0
            for i in select_files:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    t = translateThread(cnt, i, target_language, source_language,
                                        self.multiTranslateCheckBox.isChecked(), self.backupCheckBox.isChecked())
                    t.start()
                    translate_threads.append(t)
                    cnt = cnt + 1
            select_dir = self.selectDirText.toPlainText()
            if len(select_dir) > 0:
                select_dir = select_dir.replace('file:///', '')
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    paths = os.walk(select_dir, topdown=False)
                    for path, dir_lst, file_lst in paths:
                        for file_name in file_lst:
                            i = os.path.join(path, file_name)
                            if not file_name.endswith("rpy"):
                                continue
                            # _thread.start_new_thread(TranslateFile,(i,))
                            t = translateThread(cnt, i, target_language, source_language,
                                                self.multiTranslateCheckBox.isChecked(),
                                                self.backupCheckBox.isChecked())
                            t.start()
                            translate_threads.append(t)
                            cnt = cnt + 1
            if len(translate_threads) > 0:
                open('translating', "w")
                self.translateBtn.setText('translating...')
                self.translateBtn.setDisabled(True)
                _thread.start_new_thread(self.translate_threads_over, ())
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')

    @staticmethod
    def translate_threads_over():
        for t in translate_threads:
            t.join()
        log_print('translate all complete!')
        if os.path.isfile('translating'):
            os.remove('translating')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec())
