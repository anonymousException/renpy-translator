import os.path

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QFileDialog

from html_converter import Ui_HtmlConverterDialog
from html_util import plain_text_to_html


class MyHtmlConverterForm(QDialog, Ui_HtmlConverterDialog):
    def __init__(self, parent=None):
        super(MyHtmlConverterForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.setWindowIcon(QIcon('main.ico'))
        self.selectFilesBtn.clicked.connect(self.select_file)
        self.convertBtn.clicked.connect(self.on_convert_button_clicked)

    def on_convert_button_clicked(self):
        select_files = self.selectFilesText.toPlainText().split('\n')
        for i in select_files:
            i = i.replace('file:///', '')
            if len(i) > 0 and os.path.isfile(i):
                save_file_name = os.path.splitext(i)[0] + '.html'
                plain_text_to_html(i, save_file_name, self.replaceCheckBox.isChecked())

    def select_file(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       QCoreApplication.translate('HtmlConverterDialog',
                                                                                  'select the file(s) you want to convert',
                                                                                  None),
                                                       '',
                                                       "Txt Files (*.txt);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText.setText(s.rstrip('\n'))
