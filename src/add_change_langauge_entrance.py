# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_change_langauge_entrance.ui'
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

class Ui_AddEntranceDialog(object):
    def setupUi(self, AddEntranceDialog):
        if not AddEntranceDialog.objectName():
            AddEntranceDialog.setObjectName(u"AddEntranceDialog")
        AddEntranceDialog.resize(869, 212)
        self.selectFileBtn = QPushButton(AddEntranceDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(750, 30, 81, 91))
        self.selectFileBtn.setText(u"...")
        self.label = QLabel(AddEntranceDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 45, 71, 61))
        self.label.setWordWrap(True)
        self.selectFileText = QTextEdit(AddEntranceDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(70, 30, 681, 91))
        self.addEntranceCheckBox = QCheckBox(AddEntranceDialog)
        self.addEntranceCheckBox.setObjectName(u"addEntranceCheckBox")
        self.addEntranceCheckBox.setGeometry(QRect(30, 160, 801, 20))

        self.retranslateUi(AddEntranceDialog)

        QMetaObject.connectSlotsByName(AddEntranceDialog)
    # setupUi

    def retranslateUi(self, AddEntranceDialog):
        AddEntranceDialog.setWindowTitle(QCoreApplication.translate("AddEntranceDialog", u"Add change language entrance", None))
        self.label.setText(QCoreApplication.translate("AddEntranceDialog", u"file", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("AddEntranceDialog", u"Input or choose or drag the game you want to add entrance.Example:F:/DemoGame.exe", None))
        self.addEntranceCheckBox.setText(QCoreApplication.translate("AddEntranceDialog", u"Add an entrance to change language in preference option", None))
    # retranslateUi

