# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'extraction_runtime.ui'
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

class Ui_ExtractionRuntimeDialog(object):
    def setupUi(self, ExtractionRuntimeDialog):
        if not ExtractionRuntimeDialog.objectName():
            ExtractionRuntimeDialog.setObjectName(u"ExtractionRuntimeDialog")
        ExtractionRuntimeDialog.resize(666, 351)
        self.label_8 = QLabel(ExtractionRuntimeDialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(30, 165, 71, 31))
        self.label_8.setWordWrap(True)
        self.tlNameText = QTextEdit(ExtractionRuntimeDialog)
        self.tlNameText.setObjectName(u"tlNameText")
        self.tlNameText.setGeometry(QRect(110, 155, 491, 81))
        self.emptyCheckBox = QCheckBox(ExtractionRuntimeDialog)
        self.emptyCheckBox.setObjectName(u"emptyCheckBox")
        self.emptyCheckBox.setGeometry(QRect(30, 255, 501, 20))
        self.label = QLabel(ExtractionRuntimeDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 55, 71, 61))
        self.label.setWordWrap(True)
        self.selectFileBtn = QPushButton(ExtractionRuntimeDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(520, 40, 81, 91))
        self.selectFileText = QTextEdit(ExtractionRuntimeDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(110, 40, 411, 91))
        self.extractBtn = QPushButton(ExtractionRuntimeDialog)
        self.extractBtn.setObjectName(u"extractBtn")
        self.extractBtn.setGeometry(QRect(110, 310, 491, 24))

        self.retranslateUi(ExtractionRuntimeDialog)

        QMetaObject.connectSlotsByName(ExtractionRuntimeDialog)
    # setupUi

    def retranslateUi(self, ExtractionRuntimeDialog):
        ExtractionRuntimeDialog.setWindowTitle(QCoreApplication.translate("ExtractionRuntimeDialog", u"Runtime Extraction", None))
        self.label_8.setText(QCoreApplication.translate("ExtractionRuntimeDialog", u"tl name", None))
        self.tlNameText.setPlaceholderText(QCoreApplication.translate("ExtractionRuntimeDialog", u"Input the directory name under game\\tl  Example: 'japanese' or 'chinese'.If the folder already exists, the content will be appended to the original file", None))
        self.emptyCheckBox.setText(QCoreApplication.translate("ExtractionRuntimeDialog", u"Generate empty strings instead of original", None))
        self.label.setText(QCoreApplication.translate("ExtractionRuntimeDialog", u"file", None))
        self.selectFileBtn.setText(QCoreApplication.translate("ExtractionRuntimeDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("ExtractionRuntimeDialog", u"input or choose or drag the game you want to extract it's dialogues.Example:F:/DemoGame.exe", None))
        self.extractBtn.setText(QCoreApplication.translate("ExtractionRuntimeDialog", u"extract", None))
    # retranslateUi

