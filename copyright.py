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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(520, 355)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 491, 81))
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 80, 341, 31))
        self.label_2.setFont(font)
        self.url_label = QLabel(Dialog)
        self.url_label.setObjectName(u"url_label")
        self.url_label.setGeometry(QRect(150, 130, 221, 41))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setUnderline(True)
        self.url_label.setFont(font1)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 160, 481, 221))
        font2 = QFont()
        font2.setPointSize(12)
        self.label_3.setFont(font2)
        self.label_3.setWordWrap(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"CopyRight", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"The software is completely free and open-source", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"You can view the source code from ", None))
        self.url_label.setText(QCoreApplication.translate("Dialog", u"https://github.com/", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"This item is available for research and study. In no event shall the author or copyright holder be liable for any claims, damages, or other liabilities arising out of or in connection with the software or the use of the software or other dealings with the software, whether in an action in contract, an action for infringement, or any other proceeding", None))
    # retranslateUi

