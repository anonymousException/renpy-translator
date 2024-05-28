# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'extraction.ui'
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

class Ui_ExtractionDialog(object):
    def setupUi(self, ExtractionDialog):
        if not ExtractionDialog.objectName():
            ExtractionDialog.setObjectName(u"ExtractionDialog")
        ExtractionDialog.resize(652, 472)
        self.widget_2 = QWidget(ExtractionDialog)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(20, 10, 600, 451))
        self.widget_2.setMinimumSize(QSize(600, 430))
        self.selectFilesText_2 = QTextEdit(self.widget_2)
        self.selectFilesText_2.setObjectName(u"selectFilesText_2")
        self.selectFilesText_2.setGeometry(QRect(80, 30, 411, 61))
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 45, 71, 31))
        self.label_5.setWordWrap(True)
        self.selectFilesBtn_2 = QPushButton(self.widget_2)
        self.selectFilesBtn_2.setObjectName(u"selectFilesBtn_2")
        self.selectFilesBtn_2.setGeometry(QRect(490, 30, 81, 61))
        self.label_6 = QLabel(self.widget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(260, 10, 141, 20))
        font = QFont()
        font.setBold(True)
        self.label_6.setFont(font)
        self.selectDirBtn_2 = QPushButton(self.widget_2)
        self.selectDirBtn_2.setObjectName(u"selectDirBtn_2")
        self.selectDirBtn_2.setGeometry(QRect(490, 170, 81, 61))
        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(0, 180, 71, 31))
        self.label_7.setWordWrap(True)
        self.selectDirText_2 = QTextEdit(self.widget_2)
        self.selectDirText_2.setObjectName(u"selectDirText_2")
        self.selectDirText_2.setGeometry(QRect(80, 170, 411, 61))
        self.extractBtn = QPushButton(self.widget_2)
        self.extractBtn.setObjectName(u"extractBtn")
        self.extractBtn.setGeometry(QRect(84, 420, 411, 24))
        self.label_8 = QLabel(self.widget_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(0, 250, 71, 31))
        self.label_8.setWordWrap(True)
        self.tlNameText = QTextEdit(self.widget_2)
        self.tlNameText.setObjectName(u"tlNameText")
        self.tlNameText.setGeometry(QRect(80, 240, 491, 81))
        self.label_13 = QLabel(self.widget_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(0, 110, 81, 31))
        self.label_13.setWordWrap(True)
        self.selectDirsText = QTextEdit(self.widget_2)
        self.selectDirsText.setObjectName(u"selectDirsText")
        self.selectDirsText.setGeometry(QRect(80, 100, 411, 61))
        self.selectDirsBtn = QPushButton(self.widget_2)
        self.selectDirsBtn.setObjectName(u"selectDirsBtn")
        self.selectDirsBtn.setGeometry(QRect(490, 100, 81, 61))
        self.filterCheckBox = QCheckBox(self.widget_2)
        self.filterCheckBox.setObjectName(u"filterCheckBox")
        self.filterCheckBox.setGeometry(QRect(0, 330, 261, 20))
        self.label_14 = QLabel(self.widget_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(260, 332, 201, 16))
        self.label_14.setAlignment(Qt.AlignCenter)
        self.filterLengthLineEdit = QLineEdit(self.widget_2)
        self.filterLengthLineEdit.setObjectName(u"filterLengthLineEdit")
        self.filterLengthLineEdit.setGeometry(QRect(470, 330, 31, 20))
        self.emptyCheckBox = QCheckBox(self.widget_2)
        self.emptyCheckBox.setObjectName(u"emptyCheckBox")
        self.emptyCheckBox.setGeometry(QRect(0, 390, 601, 20))
        self.underlineCheckBox = QCheckBox(self.widget_2)
        self.underlineCheckBox.setObjectName(u"underlineCheckBox")
        self.underlineCheckBox.setGeometry(QRect(0, 360, 601, 20))
        self.underlineCheckBox.setChecked(True)

        self.retranslateUi(ExtractionDialog)

        QMetaObject.connectSlotsByName(ExtractionDialog)
    # setupUi

    def retranslateUi(self, ExtractionDialog):
        ExtractionDialog.setWindowTitle(QCoreApplication.translate("ExtractionDialog", u"Extraction", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText_2.setPlaceholderText(QCoreApplication.translate("ExtractionDialog", u"input or choose or drag the file(s) you want to extract here.    Examaple : F:\\GameName\\game\\script.rpy", None))
        self.label_5.setText(QCoreApplication.translate("ExtractionDialog", u"file(s)", None))
        self.selectFilesBtn_2.setText(QCoreApplication.translate("ExtractionDialog", u"...", None))
        self.label_6.setText(QCoreApplication.translate("ExtractionDialog", u"extraction", None))
        self.selectDirBtn_2.setText(QCoreApplication.translate("ExtractionDialog", u"...", None))
        self.label_7.setText(QCoreApplication.translate("ExtractionDialog", u"tl directory", None))
        self.selectDirText_2.setPlaceholderText(QCoreApplication.translate("ExtractionDialog", u"input or choose or drag the directory you want to translate here.  Example:F:\\GameName\\game\\tl\\language", None))
        self.extractBtn.setText(QCoreApplication.translate("ExtractionDialog", u"extract", None))
        self.label_8.setText(QCoreApplication.translate("ExtractionDialog", u"tl name", None))
        self.tlNameText.setPlaceholderText(QCoreApplication.translate("ExtractionDialog", u"only force needs in file(s)/directory(s) mode , for tl directory , fill nothing is acceptable. input the directory name under game\\tl  Example: japanese or chinese", None))
        self.label_13.setText(QCoreApplication.translate("ExtractionDialog", u"directory(s)", None))
#if QT_CONFIG(tooltip)
        self.selectDirsText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectDirsText.setPlaceholderText(QCoreApplication.translate("ExtractionDialog", u"input or choose or drag the directory(s) you want to extract here.    Examaple : F:\\GameName\\game\\character", None))
        self.selectDirsBtn.setText(QCoreApplication.translate("ExtractionDialog", u"...", None))
        self.filterCheckBox.setText(QCoreApplication.translate("ExtractionDialog", u"Enable filter for extract", None))
        self.label_14.setText(QCoreApplication.translate("ExtractionDialog", u"filter length less than", None))
        self.emptyCheckBox.setText(QCoreApplication.translate("ExtractionDialog", u"Generate empty strings instead of original", None))
        self.underlineCheckBox.setText(QCoreApplication.translate("ExtractionDialog", u"Skip extract the contents which include underline", None))
    # retranslateUi

