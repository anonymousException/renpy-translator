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
from extraction_official_form import MyExtractionOfficialForm
from html_converter_form import MyHtmlConverterForm

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
os.environ['NO_PROXY'] = '*'
from local_glossary_form import MyLocalGlossaryForm
from font_replace_form import MyFontReplaceForm
from game_unpacker_form import MyGameUnpackerForm
from extraction_form import MyExtractionForm
from extract_runtime_form import MyExtractionRuntimeForm
from add_change_language_entrance_form import MyAddChangeLanguageEntranceForm
from one_key_translate_form import MyOneKeyTranslateForm
from renpy_translate import translateThread, translate_threads, engineList, engineDic, language_header
from proxy import Ui_ProxyDialog
from engine import Ui_EngineDialog
from ui import Ui_MainWindow
from custom_engine_form import MyCustomEngineForm
from editor_form import MyEditorForm
from engine_form import MyEngineForm
from qt_material import apply_stylesheet

targetDic = dict()
sourceDic = dict()
translator = QTranslator()


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


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('main.ico'))
        self.selectFilesBtn.clicked.connect(self.select_file)
        self.selectDirBtn.clicked.connect(self.select_directory)
        self.translateBtn.clicked.connect(self.translate)
        self.clearLogBtn.clicked.connect(self.clear_log)
        self.translating = False
        self.extracting = False
        self.local_glossary = None
        self.localGlossaryCheckBox.clicked.connect(self.on_local_glossary_checkbox_state_changed)
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.originalRadioButton, 1)
        self.buttonGroup.addButton(self.currentRadioButton, 2)
        self.is_current = True
        self.buttonGroup.buttonClicked.connect(self.button_group_clicked)
        self.local_glossary_form = MyLocalGlossaryForm(parent=self)
        try:
            self.init_combobox()
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
        self.versionLabel.setStyleSheet("color:grey")
        self.copyrightLabel.setStyleSheet("color:grey")
        self.myExtractionForm = None
        self.myGameUnpackerForm = None
        self.myExtractionRuntimeForm = None
        self.myAddChangeLanguageEntranceForm = None
        self.myOneKeyTranslateForm = None
        self.editor_form = None
        self.myFontReplaceForm = None
        self.myExtractionOfficialForm = None
        self.myHtmlConverterForm = None
        self.actioncopyright.triggered.connect(lambda: self.show_copyright_form())
        self.proxySettings.triggered.connect(lambda: self.show_proxy_settings())
        self.engineSettings.triggered.connect(lambda: self.show_engine_settings())
        self.customEngineSettings.triggered.connect(lambda: self.show_custom_engine_settings())
        self.actionedit.triggered.connect(lambda: self.show_edit_form())
        self.actionextract_translation.triggered.connect(lambda: self.show_extraction_form())
        self.actionruntime_extraction.triggered.connect(lambda: self.show_extraction_runtime_form())
        self.actionreplace_font.triggered.connect(lambda: self.replace_font())
        self.actionunpack_game.triggered.connect(lambda: self.unpack_game())
        self.actionadd_change_langauge_entrance.triggered.connect(lambda: self.show_add_entrance_form())
        self.actionone_key_translate.triggered.connect(lambda: self.show_one_key_translate_form())
        self.actionofficial_extraction.triggered.connect(lambda: self.show_extraction_official_form())
        self.actionconvert_txt_to_html.triggered.connect(lambda: self.show_html_converter_form())
        self.actionArabic.triggered.connect(lambda: self.to_language('arabic'))
        self.actionBengali.triggered.connect(lambda: self.to_language('bengali'))
        self.actionChinese.triggered.connect(lambda: self.to_language('chinese'))
        self.actionEnglish.triggered.connect(lambda: self.switch_to_default_language())
        self.actionFrench.triggered.connect(lambda: self.to_language('french'))
        self.actionGerman.triggered.connect(lambda: self.to_language('german'))
        self.actionHindi.triggered.connect(lambda: self.to_language('hindi'))
        self.actionJapanese.triggered.connect(lambda: self.to_language('japanese'))
        self.actionKorean.triggered.connect(lambda: self.to_language('korean'))
        self.actionPortuguese.triggered.connect(lambda: self.to_language('portuguese'))
        self.actionRussian.triggered.connect(lambda: self.to_language('russian'))
        self.actionSpanish.triggered.connect(lambda: self.to_language('spanish'))
        self.actionUrdu.triggered.connect(lambda: self.to_language('urdu'))

        self.actionlight_amber.triggered.connect(lambda: self.change_theme(self.actionlight_amber.text()))
        self.actionlight_blue.triggered.connect(lambda: self.change_theme(self.actionlight_blue.text()))
        self.actionlight_cyan.triggered.connect(lambda: self.change_theme(self.actionlight_cyan.text()))
        self.actionlight_cyan_500.triggered.connect(lambda: self.change_theme(self.actionlight_cyan_500.text()))
        self.actionlight_lightgreen.triggered.connect(lambda: self.change_theme(self.actionlight_lightgreen.text()))
        self.actionlight_pink.triggered.connect(lambda: self.change_theme(self.actionlight_pink.text()))
        self.actionlight_purple.triggered.connect(lambda: self.change_theme(self.actionlight_purple.text()))
        self.actionlight_red.triggered.connect(lambda: self.change_theme(self.actionlight_red.text()))
        self.actionlight_teal.triggered.connect(lambda: self.change_theme(self.actionlight_teal.text()))
        self.actionlight_yellow.triggered.connect(lambda: self.change_theme(self.actionlight_yellow.text()))
        self.actiondark_amber.triggered.connect(lambda: self.change_theme(self.actiondark_amber.text()))
        self.actiondark_blue.triggered.connect(lambda: self.change_theme(self.actiondark_blue.text()))
        self.actiondark_cyan.triggered.connect(lambda: self.change_theme(self.actiondark_cyan.text()))
        self.actiondark_lightgreen.triggered.connect(lambda: self.change_theme(self.actiondark_lightgreen.text()))
        self.actiondark_pink.triggered.connect(lambda: self.change_theme(self.actiondark_pink.text()))
        self.actiondark_purple.triggered.connect(lambda: self.change_theme(self.actiondark_purple.text()))
        self.actiondark_red.triggered.connect(lambda: self.change_theme(self.actiondark_red.text()))
        self.actiondark_teal.triggered.connect(lambda: self.change_theme(self.actiondark_teal.text()))
        self.actiondark_yellow.triggered.connect(lambda: self.change_theme(self.actiondark_yellow.text()))

        _thread.start_new_thread(self.update_log, ())

    def show_html_converter_form(self):
        if self.myHtmlConverterForm is None:
            self.myHtmlConverterForm = MyHtmlConverterForm(parent=self)
        self.myHtmlConverterForm.exec()

    def show_extraction_official_form(self):
        if self.myExtractionOfficialForm is None:
            self.myExtractionOfficialForm = MyExtractionOfficialForm(parent=self)
        self.myExtractionOfficialForm.exec()

    def show_one_key_translate_form(self):
        self.hide()
        self.widget.hide()
        self.menubar.hide()
        self.versionLabel.hide()
        if self.myOneKeyTranslateForm is None:
            self.myOneKeyTranslateForm = MyOneKeyTranslateForm(parent=self)
        self.myOneKeyTranslateForm.parent = self
        self.myOneKeyTranslateForm.showNormal()
        self.myOneKeyTranslateForm.raise_()
        self.actionone_key_translate.triggered.disconnect()

    def show_add_entrance_form(self):
        if self.myAddChangeLanguageEntranceForm is None:
            self.myAddChangeLanguageEntranceForm = MyAddChangeLanguageEntranceForm(parent=self)
        self.myAddChangeLanguageEntranceForm.exec()

    def show_extraction_runtime_form(self):
        if self.myExtractionRuntimeForm is None:
            self.myExtractionRuntimeForm = MyExtractionRuntimeForm(parent=self)
        self.myExtractionRuntimeForm.exec()

    def show_extraction_form(self):
        if self.myExtractionForm is None:
            self.myExtractionForm = MyExtractionForm(parent=self)
            self.myExtractionForm.parent = self
        self.myExtractionForm.exec()

    def change_theme(self, new_theme):
        if new_theme is None:
            apply_stylesheet(self.app, theme=self.actionlight_blue.text() + '.xml')
            return
        apply_stylesheet(self.app, theme=new_theme + '.xml')
        f = io.open('theme', 'w', encoding='utf-8')
        f.write(new_theme)
        f.close()

    def unpack_game(self):
        if self.myGameUnpackerForm is None:
            self.myGameUnpackerForm = MyGameUnpackerForm(parent=self)
        self.myGameUnpackerForm.exec()

    def replace_font(self):
        if self.myFontReplaceForm is None:
            self.myFontReplaceForm = MyFontReplaceForm(parent=self)
        self.myFontReplaceForm.exec()

    def button_group_clicked(self, item):
        if item.group().checkedId() == 1:
            self.is_current = False
        else:
            self.is_current = True

    def on_local_glossary_checkbox_state_changed(self):
        if self.localGlossaryCheckBox.isChecked():
            self.local_glossary_form.exec()
            dic = self.local_glossary_form.data
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

    def retranslate_ui(self):
        self.retranslateUi(self)
        if self.editor_form is not None:
            self.editor_form.retranslateUi(self.editor_form)
            if self.editor_form.myImportHtmlForm is not None:
                self.editor_form.myImportHtmlForm.retranslateUi(self.editor_form.myImportHtmlForm)
            if self.editor_form.myExportXlsxSettingForm is not None:
                self.editor_form.myExportXlsxSettingForm.retranslateUi(self.editor_form.myExportXlsxSettingForm)
        if self.myGameUnpackerForm is not None:
            self.myGameUnpackerForm.retranslateUi(self.myGameUnpackerForm)
        if self.local_glossary_form is not None:
            self.local_glossary_form.retranslateUi(self.local_glossary_form)
        if self.myExtractionRuntimeForm is not None:
            self.myExtractionRuntimeForm.retranslateUi(self.myExtractionRuntimeForm)
        if self.myFontReplaceForm is not None:
            self.myFontReplaceForm.retranslateUi(self.myFontReplaceForm)
        if self.myOneKeyTranslateForm is not None:
            self.myOneKeyTranslateForm.retranslateUi(self.myOneKeyTranslateForm)
        if self.myAddChangeLanguageEntranceForm is not None:
            self.myAddChangeLanguageEntranceForm.retranslateUi(self.myAddChangeLanguageEntranceForm)
        if self.myExtractionForm is not None:
            self.myExtractionForm.retranslateUi(self.myExtractionForm)
        if self.myExtractionOfficialForm is not None:
            self.myExtractionOfficialForm.retranslateUi(self.myExtractionOfficialForm)
        if self.myHtmlConverterForm is not None:
            self.myHtmlConverterForm.retranslateUi(self.myHtmlConverterForm)

    def switch_to_default_language(self):
        app = QCoreApplication.instance()
        if app is not None:
            app.removeTranslator(translator)
            self.retranslate_ui()
            os.remove('language.txt')

    def to_language(self, lan):
        translator.load("qm/" + lan + ".qm")
        QCoreApplication.instance().installTranslator(translator)
        self.retranslate_ui()
        f = io.open("language.txt", "w", encoding='utf-8')
        f.write(lan)
        f.close()

    def show_edit_form(self):
        self.hide()
        self.widget.hide()
        self.menubar.hide()
        self.versionLabel.hide()
        if self.editor_form is None:
            self.editor_form = MyEditorForm(parent=None)
        self.editor_form.parent = self
        self.editor_form.showNormal()
        self.editor_form.raise_()
        self.actionedit.triggered.disconnect()
        # self.show()

    def show_custom_engine_settings(self):
        custom_engine_form = MyCustomEngineForm(parent=self)
        custom_engine_form.exec()

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
        if self.translating:
            self.translateBtn.setText(QCoreApplication.translate('MainWindow', 'translating...', None))
            self.translateBtn.setDisabled(True)
        else:
            self.translateBtn.setText(QCoreApplication.translate('MainWindow', 'translate', None))
            self.translateBtn.setEnabled(True)

        if self.extracting:
            if self.myExtractionForm is not None:
                self.myExtractionForm.extractBtn.setText(
                    QCoreApplication.translate('MainWindow', 'extracting...', None))
                self.myExtractionForm.extractBtn.setDisabled(True)
        else:
            if self.myExtractionForm is not None:
                self.myExtractionForm.extractBtn.setText(QCoreApplication.translate('MainWindow', 'extract', None))
                self.myExtractionForm.extractBtn.setEnabled(True)

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

    def select_file(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       QCoreApplication.translate('MainWindow',
                                                                                  'select the file(s) you want to translate',
                                                                                  None),
                                                       '',
                                                       "Rpy Files (*.rpy);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText.setText(s.rstrip('\n'))

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('MainWindow',
                                                                                      'select the directory you want to translate',
                                                                                      None))
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
                                        self.multiTranslateCheckBox.isChecked(), self.backupCheckBox.isChecked(),
                                        self.local_glossary, self.is_current, self.skipTranslatedCheckBox.isChecked())
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
                                                self.backupCheckBox.isChecked(), self.local_glossary, self.is_current,
                                                self.skipTranslatedCheckBox.isChecked())
                            t.start()
                            translate_threads.append(t)
                            cnt = cnt + 1
            if len(translate_threads) > 0:
                self.translateBtn.setText(QCoreApplication.translate('MainWindow', 'translating...', None))
                self.translateBtn.setDisabled(True)
                self.translating = True
                _thread.start_new_thread(self.translate_threads_over, ())
            else:
                self.translating = False
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            self.translating = False

    def translate_threads_over(self):
        threads_len = len(translate_threads)
        for t in translate_threads:
            if t.is_alive():
                t.join()
            translate_threads.remove(t)
        if threads_len > 0:
            log_print('translate all complete!')
        self.translating = False


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
    myWin.app = app
    if os.path.isfile('theme'):
        f = io.open('theme', 'r', encoding='utf-8')
        theme = f.read()
        myWin.change_theme(theme)
        f.close()
    else:
        myWin.change_theme(None)
    myWin.show()
    sys.exit(app.exec())
