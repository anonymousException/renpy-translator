import os
import subprocess

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialog, QFileDialog

from font_replace import Ui_FontReplaceDialog
from my_log import log_print
from renpy_fonts import GenGuiFonts
from font_util import get_default_font_path


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

    def select_directory3(self):
        directory = QFileDialog.getExistingDirectory(self, QCoreApplication.translate("FontReplaceDialog", "select the directory you want to extract", None))
        self.selectDirText_3.setText(directory)

    def select_font(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate("FontReplaceDialog", "select the file font which supports the translated language", None),
                                                     '',  # 起始路径
                                                     "Font Files (*.ttf || *.otf);;All Files (*)")
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
                GenGuiFonts(select_dir, font_path)

    def openFontStyleFile(self):
        select_dir = self.selectDirText_3.toPlainText()
        if len(select_dir) > 0:
            select_dir = select_dir.replace('file:///', '')
            if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                select_dir = select_dir + '/'
            command = 'notepad ' + select_dir + 'gui.rpy'
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 creationflags=0x08000000)
            p.wait()