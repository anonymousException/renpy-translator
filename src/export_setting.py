# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_setting.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_ExportSettingDialog(object):
    def setupUi(self, ExportSettingDialog):
        if not ExportSettingDialog.objectName():
            ExportSettingDialog.setObjectName(u"ExportSettingDialog")
        ExportSettingDialog.resize(592, 255)
        self.unitsCheckBox = QCheckBox(ExportSettingDialog)
        self.unitsCheckBox.setObjectName(u"unitsCheckBox")
        self.unitsCheckBox.setGeometry(QRect(10, 38, 221, 20))
        self.unitsCheckBox.setChecked(True)
        self.unitsMinLlineEdit = QLineEdit(ExportSettingDialog)
        self.unitsMinLlineEdit.setObjectName(u"unitsMinLlineEdit")
        self.unitsMinLlineEdit.setGeometry(QRect(234, 38, 132, 20))
        self.unitsMinLlineEdit.setPlaceholderText(u">=0")
        self.label = QLabel(ExportSettingDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(370, 40, 71, 16))
        self.label.setAlignment(Qt.AlignCenter)
        self.unitsMaxLineEdit = QLineEdit(ExportSettingDialog)
        self.unitsMaxLineEdit.setObjectName(u"unitsMaxLineEdit")
        self.unitsMaxLineEdit.setGeometry(QRect(450, 38, 132, 20))
        self.unitsMaxLineEdit.setPlaceholderText(u"<= MAX")
        self.label_2 = QLabel(ExportSettingDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(372, 125, 71, 16))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.translatedCheckBox = QCheckBox(ExportSettingDialog)
        self.translatedCheckBox.setObjectName(u"translatedCheckBox")
        self.translatedCheckBox.setGeometry(QRect(10, 123, 221, 20))
        self.translatedCheckBox.setChecked(True)
        self.translatedMaxLineEdit = QLineEdit(ExportSettingDialog)
        self.translatedMaxLineEdit.setObjectName(u"translatedMaxLineEdit")
        self.translatedMaxLineEdit.setGeometry(QRect(450, 123, 132, 20))
        self.translatedMaxLineEdit.setPlaceholderText(u"<=100%")
        self.translatedMinLineEdit = QLineEdit(ExportSettingDialog)
        self.translatedMinLineEdit.setObjectName(u"translatedMinLineEdit")
        self.translatedMinLineEdit.setGeometry(QRect(234, 123, 132, 20))
        self.translatedMinLineEdit.setPlaceholderText(u">=0%")
        self.confirmButton = QPushButton(ExportSettingDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setGeometry(QRect(10, 210, 571, 24))

        self.retranslateUi(ExportSettingDialog)

        QMetaObject.connectSlotsByName(ExportSettingDialog)
    # setupUi

    def retranslateUi(self, ExportSettingDialog):
        ExportSettingDialog.setWindowTitle(QCoreApplication.translate("ExportSettingDialog", u"Export Setting", None))
        self.unitsCheckBox.setText(QCoreApplication.translate("ExportSettingDialog", u"Filter the Units", None))
        self.label.setText(QCoreApplication.translate("ExportSettingDialog", u"and", None))
        self.label_2.setText(QCoreApplication.translate("ExportSettingDialog", u"and", None))
        self.translatedCheckBox.setText(QCoreApplication.translate("ExportSettingDialog", u"Filter the Translated", None))
        self.confirmButton.setText(QCoreApplication.translate("ExportSettingDialog", u"Confirm", None))
    # retranslateUi

