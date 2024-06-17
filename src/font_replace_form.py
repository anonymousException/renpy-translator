import _thread
import os
import subprocess
import threading
import time
import traceback

from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtWidgets import QDialog, QFileDialog

from font_replace import Ui_FontReplaceDialog
from my_log import log_print
from renpy_fonts import GenGuiFonts
from font_util import get_default_font_path

class replaceFontThread(threading.Thread):
    def __init__(self, select_dir, font_path, is_rtl_enabled):
        threading.Thread.__init__(self)
        self.select_dir = select_dir
        self.font_path = font_path
        self.is_rtl_enabled = is_rtl_enabled


    def run(self):
        try:
            log_print('start replace font ...')
            GenGuiFonts(self.select_dir, self.font_path, self.is_rtl_enabled)
            log_print('replace complete!')
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)

class MyFontReplaceForm(QDialog, Ui_FontReplaceDialog):
    def __init__(self, parent=None):
        super(MyFontReplaceForm, self).__init__(parent)
        self.setupUi(self)
        self.selectDirBtn_3.clicked.connect(self.select_directory3)
        self.selectFontBtn.clicked.connect(self.select_font)
        self.replaceFontBtn.clicked.connect(self.replaceFont)
        self.openFontStyleBtn.clicked.connect(self.openFontStyleFile)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        default_font = get_default_font_path()
        if default_font is not None:
            self.selectFontText.setText(default_font)
        self.replace_font_thread = None
        _thread.start_new_thread(self.update, ())

    def select_directory3(self):
        directory = QFileDialog.getExistingDirectory(self, QCoreApplication.translate("FontReplaceDialog", "select the directory you want to extract", None))
        self.selectDirText_3.setText(directory)

    def select_font(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate("FontReplaceDialog", "select the file font which supports the translated language", None),
                                                     '',
                                                     "Font Files (*.ttf || *.otf || *.ttc || *.otc || *.woff || *.woff2);;All Files (*)")
        self.selectFontText.setText(file)

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
                t = replaceFontThread(select_dir, font_path, self.rtlCheckBox.isChecked())
                self.replace_font_thread = t
                t.start()
                self.setDisabled(True)
                self.replaceFontBtn.setText(QCoreApplication.translate('FontReplaceDialog', 'is replacing font...', None))

    def openFontStyleFile(self):
        select_dir = self.selectDirText_3.toPlainText()
        if len(select_dir) > 0:
            select_dir = select_dir.replace('file:///', '')
            if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                select_dir = select_dir + '/'
            command = 'notepad ' + '"' + select_dir + 'gui.rpy' + '"'
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 creationflags=0x08000000, text=True, encoding='utf-8')
            p.wait()

    def update(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self):
        try:
            if self.replace_font_thread is not None:
                if not self.replace_font_thread.is_alive():
                    self.replaceFontBtn.setText(QCoreApplication.translate('FontReplaceDialog', 'replace font', None))
                    self.setEnabled(True)
                    self.replace_font_thread = None

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
