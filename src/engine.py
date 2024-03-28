# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'engine.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_EngineDialog(object):
    def setupUi(self, EngineDialog):
        if not EngineDialog.objectName():
            EngineDialog.setObjectName(u"EngineDialog")
        EngineDialog.resize(714, 300)
        self.engineComboBox = QComboBox(EngineDialog)
        self.engineComboBox.setObjectName(u"engineComboBox")
        self.engineComboBox.setGeometry(QRect(240, 20, 261, 22))
        self.label = QLabel(EngineDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 22, 221, 16))
        self.label.setWordWrap(True)
        self.label_2 = QLabel(EngineDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 211, 16))
        self.label_2.setWordWrap(True)
        self.keyEdit = QLineEdit(EngineDialog)
        self.keyEdit.setObjectName(u"keyEdit")
        self.keyEdit.setGeometry(QRect(240, 68, 451, 20))
        self.label_3 = QLabel(EngineDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 122, 211, 16))
        self.label_3.setWordWrap(True)
        self.secretEdit = QLineEdit(EngineDialog)
        self.secretEdit.setObjectName(u"secretEdit")
        self.secretEdit.setGeometry(QRect(240, 120, 451, 20))
        self.confirmButton = QPushButton(EngineDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setGeometry(QRect(20, 160, 671, 24))
        self.detailLabel = QLabel(EngineDialog)
        self.detailLabel.setObjectName(u"detailLabel")
        self.detailLabel.setGeometry(QRect(520, 11, 171, 41))
        font = QFont()
        font.setUnderline(True)
        self.detailLabel.setFont(font)
        self.detailLabel.setWordWrap(True)
        self.rpmEdit = QLineEdit(EngineDialog)
        self.rpmEdit.setObjectName(u"rpmEdit")
        self.rpmEdit.setGeometry(QRect(290, 210, 41, 20))
        self.label_4 = QLabel(EngineDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 210, 261, 20))
        self.label_4.setWordWrap(True)
        self.label_5 = QLabel(EngineDialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(390, 210, 221, 20))
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.rpsEdit = QLineEdit(EngineDialog)
        self.rpsEdit.setObjectName(u"rpsEdit")
        self.rpsEdit.setGeometry(QRect(620, 210, 71, 20))
        self.label_6 = QLabel(EngineDialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 240, 261, 20))
        self.label_6.setWordWrap(True)
        self.tpmEdit = QLineEdit(EngineDialog)
        self.tpmEdit.setObjectName(u"tpmEdit")
        self.tpmEdit.setGeometry(QRect(290, 240, 41, 20))
        self.modelComboBox = QComboBox(EngineDialog)
        self.modelComboBox.setObjectName(u"modelComboBox")
        self.modelComboBox.setGeometry(QRect(620, 240, 71, 22))
        self.label_7 = QLabel(EngineDialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(350, 240, 191, 20))
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setWordWrap(True)
        self.label_8 = QLabel(EngineDialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(20, 270, 131, 20))
        self.label_8.setWordWrap(True)
        self.baseUrlEdit = QLineEdit(EngineDialog)
        self.baseUrlEdit.setObjectName(u"baseUrlEdit")
        self.baseUrlEdit.setGeometry(QRect(160, 270, 531, 20))

        self.retranslateUi(EngineDialog)

        QMetaObject.connectSlotsByName(EngineDialog)
    # setupUi

    def retranslateUi(self, EngineDialog):
        EngineDialog.setWindowTitle(QCoreApplication.translate("EngineDialog", u"Translation Engine Settings", None))
        self.label.setText(QCoreApplication.translate("EngineDialog", u"Active Translation Engine:", None))
        self.label_2.setText(QCoreApplication.translate("EngineDialog", u"API_KEY:", None))
        self.label_3.setText(QCoreApplication.translate("EngineDialog", u"APP_SECRET:", None))
        self.secretEdit.setText("")
        self.confirmButton.setText(QCoreApplication.translate("EngineDialog", u"Confirm", None))
        self.detailLabel.setText(QCoreApplication.translate("EngineDialog", u"detail information", None))
        self.rpmEdit.setText(QCoreApplication.translate("EngineDialog", u"3", None))
        self.label_4.setText(QCoreApplication.translate("EngineDialog", u"RPM (requests per minute):", None))
        self.label_5.setText(QCoreApplication.translate("EngineDialog", u"RPS (requests per second):", None))
        self.rpsEdit.setText(QCoreApplication.translate("EngineDialog", u"3", None))
        self.label_6.setText(QCoreApplication.translate("EngineDialog", u"TPM (requests token limits):", None))
        self.tpmEdit.setText(QCoreApplication.translate("EngineDialog", u"40000", None))
        self.label_7.setText(QCoreApplication.translate("EngineDialog", u"model:", None))
        self.label_8.setText(QCoreApplication.translate("EngineDialog", u"base_url:", None))
        self.baseUrlEdit.setText("")
        self.baseUrlEdit.setPlaceholderText(QCoreApplication.translate("EngineDialog", u"http://my.test.server.example.com:8083", None))
    # retranslateUi

