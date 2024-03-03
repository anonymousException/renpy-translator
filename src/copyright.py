# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'copyright.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QWidget)

class Ui_CopyrightDialog(object):
    def setupUi(self, CopyrightDialog):
        if not CopyrightDialog.objectName():
            CopyrightDialog.setObjectName(u"CopyrightDialog")
        CopyrightDialog.resize(667, 355)
        self.label = QLabel(CopyrightDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 10, 491, 81))
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label_2 = QLabel(CopyrightDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(160, 80, 341, 31))
        self.label_2.setFont(font)
        self.url_label = QLabel(CopyrightDialog)
        self.url_label.setObjectName(u"url_label")
        self.url_label.setGeometry(QRect(40, 130, 591, 41))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setUnderline(True)
        self.url_label.setFont(font1)
        self.label_3 = QLabel(CopyrightDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(80, 160, 481, 221))
        font2 = QFont()
        font2.setPointSize(12)
        self.label_3.setFont(font2)
        self.label_3.setWordWrap(True)

        self.retranslateUi(CopyrightDialog)

        QMetaObject.connectSlotsByName(CopyrightDialog)
    # setupUi

    def retranslateUi(self, CopyrightDialog):
        CopyrightDialog.setWindowTitle(QCoreApplication.translate("CopyrightDialog", u"CopyRight", None))
        self.label.setText(QCoreApplication.translate("CopyrightDialog", u"The software is completely free and open-source", None))
        self.label_2.setText(QCoreApplication.translate("CopyrightDialog", u"You can view the source code from ", None))
        self.url_label.setText(QCoreApplication.translate("CopyrightDialog", u"https://github.com/anonymousException/renpy-translator", None))
        self.label_3.setText(QCoreApplication.translate("CopyrightDialog", u"This item is available for research and study. In no event shall the author or copyright holder be liable for any claims, damages, or other liabilities arising out of or in connection with the software or the use of the software or other dealings with the software, whether in an action in contract, an action for infringement, or any other proceeding", None))
    # retranslateUi

