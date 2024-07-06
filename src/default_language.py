# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'default_language.ui'
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

class Ui_DefaultLanguageDialog(object):
    def setupUi(self, DefaultLanguageDialog):
        if not DefaultLanguageDialog.objectName():
            DefaultLanguageDialog.setObjectName(u"DefaultLanguageDialog")
        DefaultLanguageDialog.resize(869, 267)
        self.selectFileText = QTextEdit(DefaultLanguageDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(90, 20, 661, 91))
        self.label = QLabel(DefaultLanguageDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 35, 81, 61))
        self.label.setWordWrap(True)
        self.selectFileBtn = QPushButton(DefaultLanguageDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(750, 20, 81, 91))
        self.selectFileBtn.setText(u"...")
        self.setDefaultLanguageCheckBox = QCheckBox(DefaultLanguageDialog)
        self.setDefaultLanguageCheckBox.setObjectName(u"setDefaultLanguageCheckBox")
        self.setDefaultLanguageCheckBox.setGeometry(QRect(10, 230, 821, 20))
        self.label_8 = QLabel(DefaultLanguageDialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 150, 81, 51))
        self.label_8.setWordWrap(True)
        self.tlNameText = QTextEdit(DefaultLanguageDialog)
        self.tlNameText.setObjectName(u"tlNameText")
        self.tlNameText.setGeometry(QRect(90, 140, 741, 81))

        self.retranslateUi(DefaultLanguageDialog)

        QMetaObject.connectSlotsByName(DefaultLanguageDialog)
    # setupUi

    def retranslateUi(self, DefaultLanguageDialog):
        DefaultLanguageDialog.setWindowTitle(QCoreApplication.translate("DefaultLanguageDialog", u"set default langauge at startup", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("DefaultLanguageDialog", u"Input or choose or drag the game you want to set default language at startup.Example:F:/DemoGame.exe", None))
        self.label.setText(QCoreApplication.translate("DefaultLanguageDialog", u"file", None))
        self.setDefaultLanguageCheckBox.setText(QCoreApplication.translate("DefaultLanguageDialog", u"set default language at startup", None))
        self.label_8.setText(QCoreApplication.translate("DefaultLanguageDialog", u"tl name", None))
        self.tlNameText.setPlaceholderText(QCoreApplication.translate("DefaultLanguageDialog", u"Input the directory name under game\\tl  Example: 'japanese' or 'chinese'", None))
    # retranslateUi

