# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'proxy.ui'
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

class Ui_ProxyDialog(object):
    def setupUi(self, ProxyDialog):
        if not ProxyDialog.objectName():
            ProxyDialog.setObjectName(u"ProxyDialog")
        ProxyDialog.resize(594, 93)
        self.checkBox = QCheckBox(ProxyDialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(20, 20, 161, 20))
        self.proxyEdit = QLineEdit(ProxyDialog)
        self.proxyEdit.setObjectName(u"proxyEdit")
        self.proxyEdit.setGeometry(QRect(300, 20, 271, 20))
        self.label = QLabel(ProxyDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(180, 10, 121, 41))
        self.label.setWordWrap(True)
        self.confirmButton = QPushButton(ProxyDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setGeometry(QRect(14, 60, 561, 24))

        self.retranslateUi(ProxyDialog)

        QMetaObject.connectSlotsByName(ProxyDialog)
    # setupUi

    def retranslateUi(self, ProxyDialog):
        ProxyDialog.setWindowTitle(QCoreApplication.translate("ProxyDialog", u"ProxySettings", None))
        self.checkBox.setText(QCoreApplication.translate("ProxyDialog", u"Enable Proxy", None))
        self.proxyEdit.setPlaceholderText(QCoreApplication.translate("ProxyDialog", u"example : http://localhost:10809", None))
        self.label.setText(QCoreApplication.translate("ProxyDialog", u"proxy address:", None))
        self.confirmButton.setText(QCoreApplication.translate("ProxyDialog", u"confirm", None))
    # retranslateUi

