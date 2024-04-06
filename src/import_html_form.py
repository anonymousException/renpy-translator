from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from import_html import Ui_ImportHtmlDialog
import html_util

class MyImportHtmlForm(QDialog, Ui_ImportHtmlDialog):
    def __init__(self, parent=None):
        super(MyImportHtmlForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectHtmlFileBtn.clicked.connect(self.select_html_file)
        self.selectTranslatedFileBtn.clicked.connect(self.select_translated_file)
        self.importBtn.clicked.connect(self.on_import_button_clicked)
        self.dic = None

    def on_import_button_clicked(self):
        self.dic = None
        html_file = self.selecHtmlFileText.toPlainText()
        html_file = html_file.replace('file:///', '')
        if len(html_file) == 0:
            return
        translated_file = self.selectTranslatedFileText.toPlainText()
        translated_file = translated_file.replace('file:///', '')
        if len(translated_file) == 0:
            return
        dic = html_util.get_translated_dic(html_file, translated_file)
        self.dic = dic
        if self.dic is None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('o(≧口≦)o')
            msg_box.setText(
                QCoreApplication.translate('ImportHtmlDialog', 'The html file does not match the translated file , please check the input files', None))
            msg_box.exec()
            return
        self.close()

    def select_translated_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                       QCoreApplication.translate('ImportHtmlDialog',
                                                                                  'select the relative translated file',
                                                                                  None),
                                                       '',
                                                       "Txt Files (*.txt);;All Files (*)")

        self.selectTranslatedFileText.setText(file)


    def select_html_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                       QCoreApplication.translate('ImportHtmlDialog',
                                                                                  'select the html file exported before',
                                                                                  None),
                                                       '',
                                                       "Html Files (*.html)")

        self.selecHtmlFileText.setText(file)
