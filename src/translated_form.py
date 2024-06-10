import os.path

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from translated import Ui_TranslatedDialog


class MyTranslatedForm(QDialog, Ui_TranslatedDialog):
    def __init__(self, parent=None):
        super(MyTranslatedForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.setWindowIcon(QIcon('main.ico'))
        self.confirmButton.clicked.connect(self.on_confirm_clicked)
        self.selectFileBtn.clicked.connect(self.on_select_clicked)
        self.selectFileText.textChanged.connect(self.on_text_changed)

    def on_confirm_clicked(self):
        self.close()

    def on_select_clicked(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate("TranslatedDialog",
                                                                                "select the translated file",
                                                                                None),
                                                     '',
                                                     "Txt Files (*.txt);;All Files (*)")
        self.selectFileText.setText(file)

    def on_text_changed(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            with open(path, 'r',encoding='utf-8') as f:
                self.plainTextEdit.setPlainText(f.read())
        else:
            self.plainTextEdit.setPlainText('')