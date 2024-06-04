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
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QWidget)

class Ui_GameUnpackerDialog(object):
    def setupUi(self, GameUnpackerDialog):
        if not GameUnpackerDialog.objectName():
            GameUnpackerDialog.setObjectName(u"GameUnpackerDialog")
        GameUnpackerDialog.resize(661, 323)
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
        self.autoCheckBox.setGeometry(QRect(20, 290, 551, 20))
        self.autoCheckBox.setChecked(True)
        self.label_2 = QLabel(GameUnpackerDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 190, 161, 16))
        self.label_2.setText(u"MAX_UNPACK_THREADS : ")
        self.maxThreadsLineEdit = QLineEdit(GameUnpackerDialog)
        self.maxThreadsLineEdit.setObjectName(u"maxThreadsLineEdit")
        self.maxThreadsLineEdit.setGeometry(QRect(200, 188, 391, 20))
        self.maxThreadsLineEdit.setPlaceholderText(u"")
        self.overwriteCheckBox = QCheckBox(GameUnpackerDialog)
        self.overwriteCheckBox.setObjectName(u"overwriteCheckBox")
        self.overwriteCheckBox.setGeometry(QRect(20, 230, 571, 20))
        self.unpackAllCheckBox = QCheckBox(GameUnpackerDialog)
        self.unpackAllCheckBox.setObjectName(u"unpackAllCheckBox")
        self.unpackAllCheckBox.setGeometry(QRect(20, 260, 631, 20))
        self.unpackAllCheckBox.setChecked(False)

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
        self.overwriteCheckBox.setText(QCoreApplication.translate("GameUnpackerDialog", u"Overwrite the rpy file if exsits", None))
        self.unpackAllCheckBox.setText(QCoreApplication.translate("GameUnpackerDialog", u"Unpack all files (if disabled only script files will be unpacked)", None))
    # retranslateUi

