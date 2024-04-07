# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'extraction_official.ui'
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

class Ui_ExtractionOfficialDialog(object):
    def setupUi(self, ExtractionOfficialDialog):
        if not ExtractionOfficialDialog.objectName():
            ExtractionOfficialDialog.setObjectName(u"ExtractionOfficialDialog")
        ExtractionOfficialDialog.resize(666, 351)
        self.selectFileBtn = QPushButton(ExtractionOfficialDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(520, 35, 81, 91))
        self.label_8 = QLabel(ExtractionOfficialDialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(30, 160, 71, 31))
        self.label_8.setWordWrap(True)
        self.selectFileText = QTextEdit(ExtractionOfficialDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(110, 35, 411, 91))
        self.extractBtn = QPushButton(ExtractionOfficialDialog)
        self.extractBtn.setObjectName(u"extractBtn")
        self.extractBtn.setGeometry(QRect(110, 305, 491, 24))
        self.tlNameText = QTextEdit(ExtractionOfficialDialog)
        self.tlNameText.setObjectName(u"tlNameText")
        self.tlNameText.setGeometry(QRect(110, 150, 491, 81))
        self.label = QLabel(ExtractionOfficialDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 50, 71, 61))
        self.label.setWordWrap(True)
        self.emptyCheckBox = QCheckBox(ExtractionOfficialDialog)
        self.emptyCheckBox.setObjectName(u"emptyCheckBox")
        self.emptyCheckBox.setGeometry(QRect(30, 250, 501, 20))

        self.retranslateUi(ExtractionOfficialDialog)

        QMetaObject.connectSlotsByName(ExtractionOfficialDialog)
    # setupUi

    def retranslateUi(self, ExtractionOfficialDialog):
        ExtractionOfficialDialog.setWindowTitle(QCoreApplication.translate("ExtractionOfficialDialog", u"Official Extraction", None))
        self.selectFileBtn.setText(QCoreApplication.translate("ExtractionOfficialDialog", u"...", None))
        self.label_8.setText(QCoreApplication.translate("ExtractionOfficialDialog", u"tl name", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("ExtractionOfficialDialog", u"input or choose or drag the game you want to extract it's dialogues.Example:F:/DemoGame.exe", None))
        self.extractBtn.setText(QCoreApplication.translate("ExtractionOfficialDialog", u"extract", None))
        self.tlNameText.setPlaceholderText(QCoreApplication.translate("ExtractionOfficialDialog", u"Input the directory name under game\\tl  Example: 'japanese' or 'chinese'.If the folder already exists, the content will be appended to the original file", None))
        self.label.setText(QCoreApplication.translate("ExtractionOfficialDialog", u"file", None))
        self.emptyCheckBox.setText(QCoreApplication.translate("ExtractionOfficialDialog", u"Generate empty strings instead of original", None))
    # retranslateUi

