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
        GameUnpackerDialog.resize(661, 217)
        self.label = QLabel(GameUnpackerDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 71, 61))
        self.label.setWordWrap(True)
        self.selectFileBtn = QPushButton(GameUnpackerDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(510, 25, 81, 91))
        self.selectFileText = QTextEdit(GameUnpackerDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(100, 25, 411, 91))
        self.unpackBtn = QPushButton(GameUnpackerDialog)
        self.unpackBtn.setObjectName(u"unpackBtn")
        self.unpackBtn.setGeometry(QRect(100, 130, 491, 24))
        self.autoCheckBox = QCheckBox(GameUnpackerDialog)
        self.autoCheckBox.setObjectName(u"autoCheckBox")
        self.autoCheckBox.setGeometry(QRect(100, 180, 551, 20))
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
        self.autoCheckBox.setText(QCoreApplication.translate("GameUnpackerDialog", u"Auto close the game after unpacked", None))
    # retranslateUi

