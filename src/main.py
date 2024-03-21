import _thread
import io
import multiprocessing
import os.path
import subprocess
import sys
import time
import traceback
import webbrowser
import json

from PySide6 import QtWidgets, QtCore
import sys

from PySide6.QtCore import Qt, QDir, QThread, Signal, QCoreApplication, QTranslator, QLocale, QLibraryInfo
from PySide6.QtGui import QIcon, QIntValidator, QTextCursor
from PySide6.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView, QDialog, QPushButton, QLineEdit, \
    QVBoxLayout, QMainWindow, QApplication, QButtonGroup

from copyright import Ui_CopyrightDialog
from my_log import log_print, log_path
from renpy_extract import extractThread, extract_threads, ExtractAllFilesInDir
from renpy_fonts import GenGuiFonts
from local_glossary_form import MyLocalGlossaryForm

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
os.environ['NO_PROXY'] = '*'
from renpy_translate import translateThread, translate_threads, engineList, engineDic, language_header
from proxy import Ui_ProxyDialog
from engine import Ui_EngineDialog
from ui import Ui_MainWindow
from custom_engine_form import MyCustomEngineForm
from editor_form import MyEditorForm
from engine_form import MyEngineForm
targetDic = dict()
sourceDic = dict()
translator = QTranslator()
editor_form = None

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
        self.filterCheckBox.setChecked(True)
        self.filterLengthLineEdit.setText('8')
        self.filterCheckBox.stateChanged.connect(self.filter_checkbox_changed)
        validator = QIntValidator()
        self.filterLengthLineEdit.setValidator(validator)
        self.local_glossary = None
        self.localGlossaryCheckBox.clicked.connect(self.on_local_glossary_checkbox_state_changed)
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.originalRadioButton, 1)
        self.buttonGroup.addButton(self.currentRadioButton, 2)
        self.is_current = True
        self.buttonGroup.buttonClicked.connect(self.button_group_clicked)
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
        self.actionedit.triggered.connect(lambda: self.show_edit_form())
        self.actionArabic.triggered.connect(lambda: self.to_language('arabic'))
        self.actionBengali.triggered.connect(lambda: self.to_language('bengali'))
        self.actionChinese.triggered.connect(lambda: self.to_language('chinese'))
        self.actionEnglish.triggered.connect(lambda: self.switch_to_default_language())
        self.actionFrench.triggered.connect(lambda: self.to_language('french'))
        self.actionHindi.triggered.connect(lambda: self.to_language('hindi'))
        self.actionJapanese.triggered.connect(lambda: self.to_language('japanese'))
        self.actionPortuguese.triggered.connect(lambda: self.to_language('portuguese'))
        self.actionRussian.triggered.connect(lambda: self.to_language('russian'))
        self.actionSpanish.triggered.connect(lambda: self.to_language('spanish'))
        self.actionUrdu.triggered.connect(lambda: self.to_language('urdu'))

        _thread.start_new_thread(self.update_log, ())
        if os.path.isfile('translating'):
            os.remove('translating')
        if os.path.isfile('extracting'):
            os.remove('extracting')

    def button_group_clicked(self, item):
        if item.group().checkedId() == 1:
            self.is_current = False
        else:
            self.is_current = True


    def on_local_glossary_checkbox_state_changed(self):
        if self.localGlossaryCheckBox.isChecked():
            local_glossary_form = MyLocalGlossaryForm(parent=self)
            local_glossary_form.exec()
            dic = local_glossary_form.data
            index = self.sourceComboBox.findText('Auto Detect')
            if dic is None or len(dic) == 0:
                self.localGlossaryCheckBox.setChecked(False)
                if 'Auto Detect' in sourceDic.keys() and index == -1:
                    self.sourceComboBox.addItem('Auto Detect')
                    index = self.sourceComboBox.findText('Auto Detect')
                    self.sourceComboBox.setCurrentIndex(index)
                self.local_glossary = None
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
            self.local_glossary = None

    def switch_to_default_language(self):
        app = QCoreApplication.instance()
        if app is not None:
            app.removeTranslator(translator)
            self.retranslateUi(self)
            if editor_form is not None:
                editor_form.retranslateUi(editor_form)
            os.remove('language.txt')

    def to_language(self,lan):
        translator.load("qm/"+lan+".qm")
        QCoreApplication.instance().installTranslator(translator)
        self.retranslateUi(self)
        if editor_form is not None:
            editor_form.retranslateUi(editor_form)
        f = io.open("language.txt","w",encoding='utf-8')
        f.write(lan)
        f.close()

    def show_edit_form(self):
        self.hide()
        self.widget.hide()
        self.widget_2.hide()
        self.widget_3.hide()
        self.menubar.hide()
        self.versionLabel.hide()
        global editor_form
        if editor_form is None:
            editor_form = MyEditorForm(parent=None)
        editor_form.parent = self
        editor_form.showNormal()
        editor_form.raise_()
        self.actionedit.triggered.disconnect()
        #self.show()

    def show_custom_engine_settings(self):
        custom_engine_form = MyCustomEngineForm(parent=self)
        custom_engine_form.exec()

    def filter_checkbox_changed(self, state):
        if self.filterCheckBox.isChecked():
            self.filterLengthLineEdit.setEnabled(True)
        else:
            self.filterLengthLineEdit.setDisabled(True)

    def closeEvent(self, event):
        if self.menubar.isHidden():
            self.hide()
            event.ignore()
            return

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
                self.extractBtn.setText(QCoreApplication.translate('MainWindow','extracting...',None))
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
            time.sleep(0.1)

    def update_progress(self, data):
        if data != self.log_text.toPlainText():
            self.log_text.setText(data)
            self.log_text.moveCursor(QTextCursor.End)
        if os.path.isfile('translating'):
            self.translateBtn.setText(QCoreApplication.translate('MainWindow','translating...',None))
            self.translateBtn.setDisabled(True)
        else:
            self.translateBtn.setText(QCoreApplication.translate('MainWindow','translate',None))
            self.translateBtn.setEnabled(True)

        if os.path.isfile('extracting'):
            self.extractBtn.setText(QCoreApplication.translate('MainWindow','extracting...',None))
            self.extractBtn.setDisabled(True)
        else:
            self.extractBtn.setText(QCoreApplication.translate('MainWindow','extract',None))
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
                                        self.multiTranslateCheckBox.isChecked(), self.backupCheckBox.isChecked(),self.local_glossary,self.is_current,self.skipTranslatedCheckBox.isChecked())
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
                                                self.backupCheckBox.isChecked(),self.local_glossary,self.is_current,self.skipTranslatedCheckBox.isChecked())
                            t.start()
                            translate_threads.append(t)
                            cnt = cnt + 1
            if len(translate_threads) > 0:
                open('translating', "w")
                self.translateBtn.setText(QCoreApplication.translate('MainWindow','translating...',None))
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
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    if os.path.isfile('language.txt'):
        f = io.open('language.txt', 'r', encoding='utf-8')
        lan = f.read()
        f.close()
        translator.load("qm/" + lan + ".qm")
        QCoreApplication.instance().installTranslator(translator)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec())
