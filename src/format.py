# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'format.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_FormatDialog(object):
    def setupUi(self, FormatDialog):
        if not FormatDialog.objectName():
            FormatDialog.setObjectName(u"FormatDialog")
        FormatDialog.resize(650, 225)
        self.widget_2 = QWidget(FormatDialog)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(30, 0, 600, 220))
        self.widget_2.setMinimumSize(QSize(600, 220))
        self.selectFilesText = QTextEdit(self.widget_2)
        self.selectFilesText.setObjectName(u"selectFilesText")
        self.selectFilesText.setGeometry(QRect(80, 30, 411, 61))
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 45, 71, 31))
        self.label_2.setWordWrap(True)
        self.selectFilesBtn = QPushButton(self.widget_2)
        self.selectFilesBtn.setObjectName(u"selectFilesBtn")
        self.selectFilesBtn.setGeometry(QRect(490, 30, 81, 61))
        self.selectFilesBtn.setText(u"...")
        self.label_1 = QLabel(self.widget_2)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setGeometry(QRect(260, 10, 141, 20))
        font = QFont()
        font.setBold(True)
        self.label_1.setFont(font)
        self.formatBtn = QPushButton(self.widget_2)
        self.formatBtn.setObjectName(u"formatBtn")
        self.formatBtn.setGeometry(QRect(84, 180, 411, 24))
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 110, 81, 31))
        self.label_3.setWordWrap(True)
        self.selectDirsText = QTextEdit(self.widget_2)
        self.selectDirsText.setObjectName(u"selectDirsText")
        self.selectDirsText.setGeometry(QRect(80, 100, 411, 61))
        self.selectDirsBtn = QPushButton(self.widget_2)
        self.selectDirsBtn.setObjectName(u"selectDirsBtn")
        self.selectDirsBtn.setGeometry(QRect(490, 100, 81, 61))
        self.selectDirsBtn.setText(u"...")

        self.retranslateUi(FormatDialog)

        QMetaObject.connectSlotsByName(FormatDialog)
    # setupUi

    def retranslateUi(self, FormatDialog):
        FormatDialog.setWindowTitle(QCoreApplication.translate("FormatDialog", u"format rpy files", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText.setPlaceholderText(QCoreApplication.translate("FormatDialog", u"input or choose or drag the file(s) you want to format here.    Examaple : F:\\GameName\\game\\tl\\language\\script.rpy", None))
        self.label_2.setText(QCoreApplication.translate("FormatDialog", u"file(s)", None))
        self.label_1.setText(QCoreApplication.translate("FormatDialog", u"format rpy files", None))
        self.formatBtn.setText(QCoreApplication.translate("FormatDialog", u"format rpy files", None))
        self.label_3.setText(QCoreApplication.translate("FormatDialog", u"directory(s)", None))
#if QT_CONFIG(tooltip)
        self.selectDirsText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectDirsText.setPlaceholderText(QCoreApplication.translate("FormatDialog", u"input or choose or drag the directory(s) you want to format here.    Examaple : F:\\GameName\\game\\tl\\language\\character", None))
    # retranslateUi

