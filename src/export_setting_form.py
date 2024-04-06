from PySide6.QtCore import Slot
from PySide6.QtGui import QIntValidator, QValidator, QDoubleValidator
from PySide6.QtWidgets import QDialog

from export_setting import Ui_ExportSettingDialog


class MyExportSettingForm(QDialog, Ui_ExportSettingDialog):
    def __init__(self, parent=None):
        super(MyExportSettingForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        validator = QDoubleValidator(0.0, 100.0, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.translatedMinLineEdit.setValidator(validator)
        self.translatedMaxLineEdit.setValidator(validator)
        validator = QIntValidator()
        self.unitsMinLlineEdit.setValidator(validator)
        self.unitsMaxLineEdit.setValidator(validator)
        self.translate_min = 0
        self.translate_max = 100
        self.confirmButton.clicked.connect(self.on_confirm_button_clicked)

        @Slot(str)
        def on_text_changed_min(text):
            try:
                value = float(text)
                if not (0.0 <= value <= 100.0):
                    self.translatedMinLineEdit.setText(str(self.translate_min))
                else:
                    self.translate_min = value
            except ValueError:
                pass

        @Slot(str)
        def on_text_changed_max(text):
            try:
                value = float(text)
                if not (0.0 <= value <= 100.0):
                    self.translatedMaxLineEdit.setText(str(self.translate_max))
                else:
                    self.translate_max = value
            except ValueError:
                pass

        self.translatedMinLineEdit.textChanged.connect(on_text_changed_min)
        self.translatedMaxLineEdit.textChanged.connect(on_text_changed_max)

    def on_confirm_button_clicked(self):
        self.close()