# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_unpacker.ui'
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

class Ui_GameUnpackerDialog(object):
    def setupUi(self, GameUnpackerDialog):
        if not GameUnpackerDialog.objectName():
            GameUnpackerDialog.setObjectName(u"GameUnpackerDialog")
        GameUnpackerDialog.resize(661, 206)
        self.label = QLabel(GameUnpackerDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 31, 31))
        self.label.setWordWrap(True)
        self.selectFileBtn = QPushButton(GameUnpackerDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(510, 25, 81, 61))
        self.selectFileText = QTextEdit(GameUnpackerDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(100, 25, 411, 61))
        self.unpackBtn = QPushButton(GameUnpackerDialog)
        self.unpackBtn.setObjectName(u"unpackBtn")
        self.unpackBtn.setGeometry(QRect(100, 100, 491, 24))
        self.cleanBtn = QPushButton(GameUnpackerDialog)
        self.cleanBtn.setObjectName(u"cleanBtn")
        self.cleanBtn.setGeometry(QRect(100, 140, 491, 24))
        self.autoCheckBox = QCheckBox(GameUnpackerDialog)
        self.autoCheckBox.setObjectName(u"autoCheckBox")
        self.autoCheckBox.setGeometry(QRect(260, 180, 331, 20))
        self.autoCheckBox.setChecked(True)

        self.retranslateUi(GameUnpackerDialog)

        QMetaObject.connectSlotsByName(GameUnpackerDialog)
    # setupUi

    def retranslateUi(self, GameUnpackerDialog):
        GameUnpackerDialog.setWindowTitle(QCoreApplication.translate("GameUnpackerDialog", u"Game Unpacker", None))
        self.label.setText(QCoreApplication.translate("GameUnpackerDialog", u"file", None))
        self.selectFileBtn.setText(QCoreApplication.translate("GameUnpackerDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("GameUnpackerDialog", u"input or choose or drag the game you want to unpack it's rpa files.Example:F:/DemoGame.exe", None))
        self.unpackBtn.setText(QCoreApplication.translate("GameUnpackerDialog", u"Unpack", None))
        self.cleanBtn.setText(QCoreApplication.translate("GameUnpackerDialog", u"Clean temporary files", None))
        self.autoCheckBox.setText(QCoreApplication.translate("GameUnpackerDialog", u"Auto Clean after unpack", None))
    # retranslateUi

