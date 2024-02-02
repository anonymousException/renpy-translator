import _thread
import io
import json
import os.path
import sys
import time
import traceback
import webbrowser

import dl_translate
import torch
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtWidgets import QDialog
from pygtrans import Translate

from copyright import Ui_CopyrightDialog
from proxy import Ui_ProxyDialog
from my_log import log_print, log_path
from renpy_extract import extractThread, extract_threads, ExtractAllFilesInDir
from renpy_fonts import GenGuiFonts
from renpy_translate import translateThread, translate_threads, clientDic
from ui import Ui_MainWindow

os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

targetDic = dict()
sourceDic = dict()
modelUrlDic = dict()
device_mode = 'auto'

def is_empty_folder(folder_path):
    contents = os.listdir(folder_path)
    if not contents:
        return True
    else:
        return False

class MyProxyForm(QDialog, Ui_ProxyDialog):
    def __init__(self, parent=None):
        super(MyProxyForm, self).__init__(parent)
        self.setupUi(self)
        if  os.path.isfile('proxy.txt'):
            with open('proxy.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                self.proxyEdit.setText(loaded_data['proxy'])
                self.checkBox.setChecked((loaded_data['enable']))
        self.confirmButton.clicked.connect(self.confirm)
    def confirm(self):
        f = io.open('proxy.txt', 'w', encoding='utf-8')
        data = {"proxy":self.proxyEdit.text(),"enable":self.checkBox.isChecked()}
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

        self.url_label.setCursor(Qt.PointingHandCursor)

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
        self.selectFontBtn.clicked.connect(self.select_font)
        self.selectFilesBtn_2.clicked.connect(self.select_file2)
        self.selectDirBtn_2.clicked.connect(self.select_directory2)
        self.selectDirBtn_3.clicked.connect(self.select_directory3)
        self.extractBtn.clicked.connect(self.extract)
        self.replaceFontBtn.clicked.connect(self.replaceFont)
        self.openFontStyleBtn.clicked.connect(self.openFontStyleFile)
        self.init_combobox()
        self.versionLabel.setStyleSheet("color:grey")
        self.copyrightLabel.setStyleSheet("color:grey")
        self.actioncopyright.triggered.connect(lambda: self.show_copyright_form())
        self.proxySettings.triggered.connect(lambda: self.showProxySettings())
        self.checkEnableAIBox.clicked.connect(self.check_enableAI)
        self.aiModelComboBox.currentIndexChanged.connect(self.aiModelComboBoxChanged)
        self.aiRunningModeComboBox.currentIndexChanged.connect(self.aiRunningModeComboBoxChanged)
        _thread.start_new_thread(self.update_log, ())

    def showProxySettings(self):
        proxy_form = MyProxyForm(parent=self)
        proxy_form.exec()

    def aiRunningModeComboBoxChanged(self,event):
        mode = self.aiRunningModeComboBox.currentText()
        device_mode = mode
        clientDic.clear()
        ori_target_index = self.targetComboBox.currentIndex()
        ori_source_index = self.sourceComboBox.currentIndex()
        self.fresh_language_combobox()
        self.targetComboBox.setCurrentIndex(ori_target_index)
        self.sourceComboBox.setCurrentIndex(ori_source_index)

    def aiModelComboBoxChanged(self, event):
        if not self.checkEnableAIBox.isChecked():
            return
        model = self.aiModelComboBox.currentText()
        self.targetComboBox.clear()
        self.sourceComboBox.clear()
        if (model == ''):
            return
        self.targetComboBox.addItem('loading')
        self.sourceComboBox.addItem('loading')
        self.targetComboBox.setDisabled(True)
        self.sourceComboBox.setDisabled(True)
        model = self.aiModelComboBox.currentText()
        if (model == ''):
            return
        modelPath = os.getcwd() + '/' + model
        if (not os.path.exists(modelPath) or is_empty_folder(modelPath)):
            reply = QMessageBox.question(self, 'Notice', 'AI-Model is not detected in '+modelPath+'! Would you like to download it?', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                log_print('Please copy all the files to:\n' + modelPath)
                QMessageBox.information(self,'Tips','Opening brower to download the model. After all files downloaded,please copy all the files to ' + modelPath + ' (You can copy the path from log)')
                if (not os.path.exists(modelPath)):
                    os.mkdir(modelPath)
                webbrowser.open(modelUrlDic[model])
            self.aiModelComboBox.setCurrentIndex(0)
            return
        _thread.start_new_thread(self.fresh_language_combobox, ())


    def fresh_language_combobox(self):
        model = self.aiModelComboBox.currentText()
        if(model == ''):
            return
        modelPath = os.getcwd()+'/'+model
        if(os.path.exists(modelPath)):
            if model in clientDic:
                 client = clientDic[model]
            else:
                client = dl_translate.TranslationModel(modelPath, device=device_mode,model_family=model)
                clientDic[model] = client
            self.targetComboBox.clear()
            self.sourceComboBox.clear()
            for i in client.available_languages():
                self.targetComboBox.addItem(i)
                self.sourceComboBox.addItem(i)
            self.targetComboBox.setCurrentIndex(0)
            self.sourceComboBox.setCurrentIndex(0)
            self.targetComboBox.setEnabled(True)
            self.sourceComboBox.setEnabled(True)


    def check_enableAI(self):
        if self.checkEnableAIBox.isChecked():
            self.aiModelComboBox.setEnabled(True)
            self.batchSizeComboBox.setEnabled(True)
            self.aiRunningModeComboBox.setEnabled(True)
            self.aiModelComboBoxChanged(None)
            self.targetComboBox.clear()
            self.sourceComboBox.clear()
        else:
            self.aiModelComboBox.setDisabled(True)
            self.batchSizeComboBox.setDisabled(True)
            self.aiRunningModeComboBox.setDisabled(True)
            self.init_combobox()

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
            d[contents[0]] = contents[1].strip()
            ret_l.append(contents[0])
        ret_l.sort()
        return ret_l

    def init_combobox(self):
        self.targetComboBox.clear()
        self.sourceComboBox.clear()
        target_l = self.get_combobox_content('target.rst', targetDic)
        for i in target_l:
            self.targetComboBox.addItem(i)
        source_l = self.get_combobox_content('source.rst', sourceDic)
        for i in source_l:
            self.sourceComboBox.addItem(i)
        self.sourceComboBox.setCurrentIndex(source_l.index('Auto Detect'))

        if self.aiModelComboBox.count() > 0:
            pass
        else:
            ai_models = ['','mbart50','m2m100','nllb200']
            ai_models_urls = ['','https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt/tree/main','https://huggingface.co/facebook/m2m100_418M/tree/main','https://huggingface.co/facebook/nllb-200-distilled-600M/tree/main']
            for i,e in enumerate(ai_models):
                self.aiModelComboBox.addItem(e)
                modelUrlDic[e] = ai_models_urls[i]

        if self.batchSizeComboBox.count() > 0:
            pass
        else:
            batch_sizes = [1,2,4,8,16,32]
            for i,e in enumerate(batch_sizes):
                self.batchSizeComboBox.addItem(str(e))
            self.batchSizeComboBox.setCurrentIndex(3)
            self.batchSizeComboBox.setDisabled(True)

        if self.aiRunningModeComboBox.count()>0:
            pass
        else:
            modes = ['auto','cpu','gpu']
            for i in modes:
                self.aiRunningModeComboBox.addItem(i)
                self.aiRunningModeComboBox.setDisabled(True)



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
                    t = extractThread(cnt, i, tl_name)
                    t.start()
                    extract_threads.append(t)
            select_dir = self.selectDirText_2.toPlainText()
            if len(select_dir) > 0:
                select_dir = select_dir.replace('file:///', '')
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    ExtractAllFilesInDir(select_dir)
                    log_print('extract directory: ' + select_dir + ' success!')
            if len(extract_threads) > 0:
                _thread.start_new_thread(self.extract_threads_over, ())
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)

    @staticmethod
    def extract_threads_over():
        for t in extract_threads:
            t.join()
        log_print('extract all complete!')

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

    class UpdateThread(QThread):
        update_date = Signal(str)

        def __init__(self):
            super().__init__()

        def __del__(self):
            self.wait()

        # 处理要做的业务逻辑
        def run(self):
            f = io.open(log_path, 'r+', encoding='utf-8')
            self.update_date.emit(f.read())
            f.close()

    def select_directory3(self):
        directory = QFileDialog.getExistingDirectory(self, 'select the directory you want to extract')
        self.selectDirText_3.setText(directory)

    def select_file2(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       "select the file(s) you want to extract",
                                                       '',  # 起始路径
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
                                                       '',  # 起始路径
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
            if self.checkEnableAIBox.isChecked():
                if self.aiModelComboBox.currentIndex() == 0:
                    return
                else:
                    currentClient = clientDic[self.aiModelComboBox.currentText()]
                    target_language = self.targetComboBox.currentText()
                    source_language = self.sourceComboBox.currentText()
            else:
                currentClient = Translate()
                with open('proxy.txt', 'r') as json_file:
                    loaded_data = json.load(json_file)
                    if loaded_data['enable']:
                        currentClient = Translate(proxies={'https': loaded_data['proxy']})
                target_language = targetDic[self.targetComboBox.currentText()]
                source_language = sourceDic[self.sourceComboBox.currentText()]
            select_files = self.selectFilesText.toPlainText().split('\n')
            batch_size = int(self.batchSizeComboBox.currentText())
            cnt = 0
            for i in select_files:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    t = translateThread(cnt, currentClient,i, target_language, source_language,batch_size)
                    t.start()
                    translate_threads.append(t)
            select_dir = self.selectDirText.toPlainText()
            if len(select_dir) > 0:
                select_dir = select_dir.replace('file:///', '')
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    paths = os.walk(select_dir)
                    for path, dir_lst, file_lst in paths:
                        for file_name in file_lst:
                            i = os.path.join(path, file_name)
                            if not file_name.endswith("rpy"):
                                continue
                            t = translateThread(cnt,currentClient, i, target_language, source_language,batch_size)
                            t.start()
                            translate_threads.append(t)
                            cnt = cnt + 1
            if len(translate_threads) > 0:
                _thread.start_new_thread(self.translate_threads_over, ())
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)

    @staticmethod
    def translate_threads_over():
        for t in translate_threads:
            t.join()
        log_print('translate all complete!')


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()

    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec())
