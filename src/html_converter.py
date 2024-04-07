# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'html_converter.ui'
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
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_HtmlConverterDialog(object):
    def setupUi(self, HtmlConverterDialog):
        if not HtmlConverterDialog.objectName():
            HtmlConverterDialog.setObjectName(u"HtmlConverterDialog")
        HtmlConverterDialog.resize(655, 197)
        self.label = QLabel(HtmlConverterDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 25, 71, 61))
        self.label.setWordWrap(True)
        self.selectFilesText = QTextEdit(HtmlConverterDialog)
        self.selectFilesText.setObjectName(u"selectFilesText")
        self.selectFilesText.setGeometry(QRect(100, 20, 411, 81))
        self.selectFilesBtn = QPushButton(HtmlConverterDialog)
        self.selectFilesBtn.setObjectName(u"selectFilesBtn")
        self.selectFilesBtn.setGeometry(QRect(510, 20, 81, 81))
        self.selectFilesBtn.setText(u"...")
        self.convertBtn = QPushButton(HtmlConverterDialog)
        self.convertBtn.setObjectName(u"convertBtn")
        self.convertBtn.setGeometry(QRect(100, 160, 491, 24))
        self.replaceCheckBox = QCheckBox(HtmlConverterDialog)
        self.replaceCheckBox.setObjectName(u"replaceCheckBox")
        self.replaceCheckBox.setGeometry(QRect(20, 120, 571, 20))
        self.replaceCheckBox.setChecked(True)

        self.retranslateUi(HtmlConverterDialog)

        QMetaObject.connectSlotsByName(HtmlConverterDialog)
    # setupUi

    def retranslateUi(self, HtmlConverterDialog):
        HtmlConverterDialog.setWindowTitle(QCoreApplication.translate("HtmlConverterDialog", u"Html Converter", None))
        self.label.setText(QCoreApplication.translate("HtmlConverterDialog", u"file(s)", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText.setPlaceholderText(QCoreApplication.translate("HtmlConverterDialog", u"input or choose or drag the file(s) you want to convert to html here. Examaple : F:\\example.txt", None))
        self.convertBtn.setText(QCoreApplication.translate("HtmlConverterDialog", u"convert", None))
        self.replaceCheckBox.setText(QCoreApplication.translate("HtmlConverterDialog", u"Replace Special Symbols", None))
    # retranslateUi

