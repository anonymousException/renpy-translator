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
        EngineDialog.resize(528, 201)
        self.engineComboBox = QComboBox(EngineDialog)
        self.engineComboBox.setObjectName(u"engineComboBox")
        self.engineComboBox.setGeometry(QRect(180, 20, 221, 22))
        self.label = QLabel(EngineDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 22, 161, 16))
        self.label_2 = QLabel(EngineDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 54, 16))
        self.keyEdit = QLineEdit(EngineDialog)
        self.keyEdit.setObjectName(u"keyEdit")
        self.keyEdit.setGeometry(QRect(100, 68, 411, 20))
        self.label_3 = QLabel(EngineDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 122, 81, 16))
        self.secretEdit = QLineEdit(EngineDialog)
        self.secretEdit.setObjectName(u"secretEdit")
        self.secretEdit.setGeometry(QRect(100, 120, 411, 20))
        self.confirmButton = QPushButton(EngineDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setGeometry(QRect(200, 160, 121, 24))
        self.detailLabel = QLabel(EngineDialog)
        self.detailLabel.setObjectName(u"detailLabel")
        self.detailLabel.setGeometry(QRect(410, 21, 111, 21))
        font = QFont()
        font.setUnderline(True)
        self.detailLabel.setFont(font)

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
    # retranslateUi

