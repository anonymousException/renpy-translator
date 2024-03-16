# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QGridLayout, QLabel, QPushButton, QRadioButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_EditorDialog(object):
    def setupUi(self, EditorDialog):
        if not EditorDialog.objectName():
            EditorDialog.setObjectName(u"EditorDialog")
        EditorDialog.resize(1254, 759)
        self.gridLayout = QGridLayout(EditorDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fileVerticalLayout = QVBoxLayout()
        self.fileVerticalLayout.setObjectName(u"fileVerticalLayout")

        self.gridLayout.addLayout(self.fileVerticalLayout, 1, 1, 3, 1)

        self.widget = QWidget(EditorDialog)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(550, 300))
        self.widget.setMaximumSize(QSize(550, 300))
        self.changeTranslationEngineButton = QPushButton(self.widget)
        self.changeTranslationEngineButton.setObjectName(u"changeTranslationEngineButton")
        self.changeTranslationEngineButton.setGeometry(QRect(20, 230, 161, 24))
        self.selectDirText = QTextEdit(self.widget)
        self.selectDirText.setObjectName(u"selectDirText")
        self.selectDirText.setGeometry(QRect(100, 75, 341, 41))
        self.targetComboBox = QComboBox(self.widget)
        self.targetComboBox.setObjectName(u"targetComboBox")
        self.targetComboBox.setGeometry(QRect(100, 150, 421, 22))
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 77, 61, 31))
        self.sourceComboBox = QComboBox(self.widget)
        self.sourceComboBox.setObjectName(u"sourceComboBox")
        self.sourceComboBox.setGeometry(QRect(100, 195, 421, 22))
        self.selectFilesBtn = QPushButton(self.widget)
        self.selectFilesBtn.setObjectName(u"selectFilesBtn")
        self.selectFilesBtn.setGeometry(QRect(440, 0, 81, 41))
        self.selectFilesText = QTextEdit(self.widget)
        self.selectFilesText.setObjectName(u"selectFilesText")
        self.selectFilesText.setGeometry(QRect(100, 0, 341, 41))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 5, 31, 31))
        self.label.setWordWrap(True)
        self.rpyCheckBox = QCheckBox(self.widget)
        self.rpyCheckBox.setObjectName(u"rpyCheckBox")
        self.rpyCheckBox.setGeometry(QRect(200, 270, 131, 20))
        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(20, 190, 41, 31))
        self.selectDirBtn = QPushButton(self.widget)
        self.selectDirBtn.setObjectName(u"selectDirBtn")
        self.selectDirBtn.setGeometry(QRect(440, 75, 81, 41))
        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 145, 41, 31))
        self.addListButton = QPushButton(self.widget)
        self.addListButton.setObjectName(u"addListButton")
        self.addListButton.setGeometry(QRect(190, 230, 151, 24))
        self.showLogButton = QPushButton(self.widget)
        self.showLogButton.setObjectName(u"showLogButton")
        self.showLogButton.setGeometry(QRect(360, 230, 151, 24))

        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)

        self.tableVerticalLayout = QVBoxLayout()
        self.tableVerticalLayout.setObjectName(u"tableVerticalLayout")

        self.gridLayout.addLayout(self.tableVerticalLayout, 1, 2, 3, 2)

        self.widget_2 = QWidget(EditorDialog)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(680, 300))
        self.currentRadioButton = QRadioButton(self.widget_2)
        self.currentRadioButton.setObjectName(u"currentRadioButton")
        self.currentRadioButton.setGeometry(QRect(420, 40, 71, 20))
        self.currentRadioButton.setMaximumSize(QSize(16777215, 20))
        self.currentRadioButton.setChecked(True)
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 40, 111, 20))
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.saveFileButton = QPushButton(self.widget_2)
        self.saveFileButton.setObjectName(u"saveFileButton")
        self.saveFileButton.setGeometry(QRect(180, 70, 335, 24))
        self.saveFileButton.setMaximumSize(QSize(16777215, 24))
        self.untranslatedCheckBox = QCheckBox(self.widget_2)
        self.untranslatedCheckBox.setObjectName(u"untranslatedCheckBox")
        self.untranslatedCheckBox.setGeometry(QRect(100, 10, 165, 20))
        self.untranslatedCheckBox.setMaximumSize(QSize(16777215, 20))
        self.originalRadioButton = QRadioButton(self.widget_2)
        self.originalRadioButton.setObjectName(u"originalRadioButton")
        self.originalRadioButton.setGeometry(QRect(320, 40, 71, 20))
        self.originalRadioButton.setMaximumSize(QSize(16777215, 20))
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 100, 601, 191))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.searchedOnlyCheckBox = QCheckBox(self.widget_2)
        self.searchedOnlyCheckBox.setObjectName(u"searchedOnlyCheckBox")
        self.searchedOnlyCheckBox.setGeometry(QRect(280, 10, 141, 20))
        self.searchedOnlyCheckBox.setMaximumSize(QSize(16777215, 20))
        self.logAfterSearchCheckBox = QCheckBox(self.widget_2)
        self.logAfterSearchCheckBox.setObjectName(u"logAfterSearchCheckBox")
        self.logAfterSearchCheckBox.setGeometry(QRect(430, 10, 151, 20))
        self.logAfterSearchCheckBox.setMaximumSize(QSize(16777215, 20))
        self.logAfterSearchCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.widget_2, 0, 2, 1, 2)


        self.retranslateUi(EditorDialog)

        QMetaObject.connectSlotsByName(EditorDialog)
    # setupUi

    def retranslateUi(self, EditorDialog):
        EditorDialog.setWindowTitle(QCoreApplication.translate("EditorDialog", u"Ren'py Translator Editor", None))
        self.changeTranslationEngineButton.setText(QCoreApplication.translate("EditorDialog", u"Change Translation Engine", None))
        self.selectDirText.setPlaceholderText(QCoreApplication.translate("EditorDialog", u"input or choose or drag the directory you want to edit here.  Example:F:\\GameName\\game\\tl\\language", None))
        self.label_2.setText(QCoreApplication.translate("EditorDialog", u"directory", None))
        self.selectFilesBtn.setText(QCoreApplication.translate("EditorDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText.setPlaceholderText(QCoreApplication.translate("EditorDialog", u"input or choose or drag the file(s) you want to edit here. Examaple : F:\\GameName\\game\\tl\\language\\script.rpy", None))
        self.label.setText(QCoreApplication.translate("EditorDialog", u"file(s)", None))
        self.rpyCheckBox.setText(QCoreApplication.translate("EditorDialog", u"Show .rpy File Only", None))
        self.label_10.setText(QCoreApplication.translate("EditorDialog", u"source", None))
        self.selectDirBtn.setText(QCoreApplication.translate("EditorDialog", u"...", None))
        self.label_9.setText(QCoreApplication.translate("EditorDialog", u"target", None))
        self.addListButton.setText(QCoreApplication.translate("EditorDialog", u"Add to file list", None))
        self.showLogButton.setText(QCoreApplication.translate("EditorDialog", u"Show Log Form", None))
        self.currentRadioButton.setText(QCoreApplication.translate("EditorDialog", u"Current", None))
        self.label_3.setText(QCoreApplication.translate("EditorDialog", u"Translation Source", None))
        self.saveFileButton.setText(QCoreApplication.translate("EditorDialog", u"Save to file", None))
        self.untranslatedCheckBox.setText(QCoreApplication.translate("EditorDialog", u"Show Untranslated Only", None))
        self.originalRadioButton.setText(QCoreApplication.translate("EditorDialog", u"Original", None))
        self.label_4.setText(QCoreApplication.translate("EditorDialog", u"<html><head/><body><p>Multi-Select is supportable (Hold down the 'Ctrl' to Active) </p><p>Besides you can use 'Shift' to select a continuous line</p><p>Select the line(s) you want to operate , right click to show menu</p><p>'Ctrl + A' to select all the lines<br/>'Ctrl + F' to search the content<br/>'Ctrl + G' to jump to line</p><p>As for save , only the contents in column 'Current' will be replaced to the file</p><p>At last , you can modify the 'Current' and 'Translated' column through  Double-Click</p></body></html>", None))
        self.searchedOnlyCheckBox.setText(QCoreApplication.translate("EditorDialog", u"Show Searched Only", None))
        self.logAfterSearchCheckBox.setText(QCoreApplication.translate("EditorDialog", u"Show Log After Search", None))
    # retranslateUi

