# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'font_replace.ui'
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

class Ui_FontReplaceDialog(object):
    def setupUi(self, FontReplaceDialog):
        if not FontReplaceDialog.objectName():
            FontReplaceDialog.setObjectName(u"FontReplaceDialog")
        FontReplaceDialog.resize(659, 276)
        self.widget_3 = QWidget(FontReplaceDialog)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(30, 20, 600, 220))
        self.widget_3.setMinimumSize(QSize(600, 220))
        self.label_11 = QLabel(self.widget_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(260, 0, 121, 20))
        font = QFont()
        font.setBold(True)
        self.label_11.setFont(font)
        self.selectFontText = QTextEdit(self.widget_3)
        self.selectFontText.setObjectName(u"selectFontText")
        self.selectFontText.setGeometry(QRect(80, 100, 411, 41))
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 105, 81, 31))
        self.label_4.setWordWrap(True)
        self.selectFontBtn = QPushButton(self.widget_3)
        self.selectFontBtn.setObjectName(u"selectFontBtn")
        self.selectFontBtn.setGeometry(QRect(490, 100, 81, 41))
        self.replaceFontBtn = QPushButton(self.widget_3)
        self.replaceFontBtn.setObjectName(u"replaceFontBtn")
        self.replaceFontBtn.setGeometry(QRect(84, 150, 411, 24))
        self.openFontStyleBtn = QPushButton(self.widget_3)
        self.openFontStyleBtn.setObjectName(u"openFontStyleBtn")
        self.openFontStyleBtn.setGeometry(QRect(80, 190, 411, 24))
        self.label_12 = QLabel(self.widget_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(0, 40, 81, 31))
        self.label_12.setWordWrap(True)
        self.selectDirText_3 = QTextEdit(self.widget_3)
        self.selectDirText_3.setObjectName(u"selectDirText_3")
        self.selectDirText_3.setGeometry(QRect(80, 38, 411, 41))
        self.selectDirBtn_3 = QPushButton(self.widget_3)
        self.selectDirBtn_3.setObjectName(u"selectDirBtn_3")
        self.selectDirBtn_3.setGeometry(QRect(490, 38, 81, 41))

        self.retranslateUi(FontReplaceDialog)

        QMetaObject.connectSlotsByName(FontReplaceDialog)
    # setupUi

    def retranslateUi(self, FontReplaceDialog):
        FontReplaceDialog.setWindowTitle(QCoreApplication.translate("FontReplaceDialog", u"Font Replace", None))
        self.label_11.setText(QCoreApplication.translate("FontReplaceDialog", u"font", None))
        self.selectFontText.setPlaceholderText(QCoreApplication.translate("FontReplaceDialog", u"input or choose or drag the font which supports the language after translation. Example : DejaVuSans.ttf (ren'py 's default font)", None))
        self.label_4.setText(QCoreApplication.translate("FontReplaceDialog", u"font", None))
        self.selectFontBtn.setText(QCoreApplication.translate("FontReplaceDialog", u"...", None))
        self.replaceFontBtn.setText(QCoreApplication.translate("FontReplaceDialog", u"replace font", None))
        self.openFontStyleBtn.setText(QCoreApplication.translate("FontReplaceDialog", u"open font style file", None))
        self.label_12.setText(QCoreApplication.translate("FontReplaceDialog", u"directory", None))
        self.selectDirText_3.setPlaceholderText(QCoreApplication.translate("FontReplaceDialog", u"input or choose or drag the directory you want to replace font here.  Example:F:\\GameName\\game\\tl\\language", None))
        self.selectDirBtn_3.setText(QCoreApplication.translate("FontReplaceDialog", u"...", None))
    # retranslateUi

