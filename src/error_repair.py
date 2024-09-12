# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_repair.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_ErrorRepairDialog(object):
    def setupUi(self, ErrorRepairDialog):
        if not ErrorRepairDialog.objectName():
            ErrorRepairDialog.setObjectName(u"ErrorRepairDialog")
        ErrorRepairDialog.resize(666, 250)
        self.selectFileBtn = QPushButton(ErrorRepairDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(530, 30, 81, 91))
        self.selectFileBtn.setText(u"...")
        self.label = QLabel(ErrorRepairDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 45, 71, 61))
        self.label.setWordWrap(True)
        self.selectFileText = QTextEdit(ErrorRepairDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(120, 30, 411, 91))
        self.selectFileText.setPlaceholderText(u"Example:F:/DemoGame.exe")
        self.label_2 = QLabel(ErrorRepairDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 150, 211, 61))
        self.label_2.setWordWrap(True)
        self.maxRecursionLineEdit = QLineEdit(ErrorRepairDialog)
        self.maxRecursionLineEdit.setObjectName(u"maxRecursionLineEdit")
        self.maxRecursionLineEdit.setGeometry(QRect(260, 170, 351, 20))
        self.maxRecursionLineEdit.setText(u"")
        self.maxRecursionLineEdit.setAlignment(Qt.AlignCenter)
        self.repairBtn = QPushButton(ErrorRepairDialog)
        self.repairBtn.setObjectName(u"repairBtn")
        self.repairBtn.setGeometry(QRect(120, 220, 491, 24))

        self.retranslateUi(ErrorRepairDialog)

        QMetaObject.connectSlotsByName(ErrorRepairDialog)
    # setupUi

    def retranslateUi(self, ErrorRepairDialog):
        ErrorRepairDialog.setWindowTitle(QCoreApplication.translate("ErrorRepairDialog", u"Error Repair", None))
        self.label.setText(QCoreApplication.translate("ErrorRepairDialog", u"file", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("ErrorRepairDialog", u"max repair count", None))
        self.repairBtn.setText(QCoreApplication.translate("ErrorRepairDialog", u"repair errors", None))
    # retranslateUi

