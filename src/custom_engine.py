# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_engine.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_CustomDialog(object):
    def setupUi(self, CustomDialog):
        if not CustomDialog.objectName():
            CustomDialog.setObjectName(u"CustomDialog")
        CustomDialog.resize(1174, 668)
        self.gridLayout = QGridLayout(CustomDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.clearLogBtn = QPushButton(CustomDialog)
        self.clearLogBtn.setObjectName(u"clearLogBtn")

        self.gridLayout.addWidget(self.clearLogBtn, 3, 1, 1, 1)

        self.widget = QWidget(CustomDialog)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(600, 650))
        self.selectScriptBtn = QPushButton(self.widget)
        self.selectScriptBtn.setObjectName(u"selectScriptBtn")
        self.selectScriptBtn.setGeometry(QRect(500, 240, 81, 41))
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(150, 510, 54, 20))
        self.nameLineEdit = QLineEdit(self.widget)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QRect(80, 65, 501, 20))
        self.customComboBox = QComboBox(self.widget)
        self.customComboBox.setObjectName(u"customComboBox")
        self.customComboBox.setGeometry(QRect(170, 5, 411, 22))
        self.renameScriptCheckBox = QCheckBox(self.widget)
        self.renameScriptCheckBox.setObjectName(u"renameScriptCheckBox")
        self.renameScriptCheckBox.setGeometry(QRect(20, 295, 111, 20))
        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(150, 405, 54, 20))
        self.renameSourceLineEdit = QLineEdit(self.widget)
        self.renameSourceLineEdit.setObjectName(u"renameSourceLineEdit")
        self.renameSourceLineEdit.setGeometry(QRect(210, 405, 371, 20))
        self.saveKeySecretCheckBox = QCheckBox(self.widget)
        self.saveKeySecretCheckBox.setObjectName(u"saveKeySecretCheckBox")
        self.saveKeySecretCheckBox.setGeometry(QRect(160, 545, 301, 21))
        self.selectScriptText = QTextEdit(self.widget)
        self.selectScriptText.setObjectName(u"selectScriptText")
        self.selectScriptText.setGeometry(QRect(80, 240, 421, 41))
        self.renameSourceCheckBox = QCheckBox(self.widget)
        self.renameSourceCheckBox.setObjectName(u"renameSourceCheckBox")
        self.renameSourceCheckBox.setGeometry(QRect(20, 405, 111, 20))
        self.renameTargetCheckBox = QCheckBox(self.widget)
        self.renameTargetCheckBox.setObjectName(u"renameTargetCheckBox")
        self.renameTargetCheckBox.setGeometry(QRect(20, 510, 111, 20))
        self.keyCheckBox = QCheckBox(self.widget)
        self.keyCheckBox.setObjectName(u"keyCheckBox")
        self.keyCheckBox.setGeometry(QRect(20, 165, 161, 20))
        self.queueCheckBox = QCheckBox(self.widget)
        self.queueCheckBox.setObjectName(u"queueCheckBox")
        self.queueCheckBox.setGeometry(QRect(20, 205, 551, 20))
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 460, 41, 31))
        self.label_7.setWordWrap(True)
        self.selectSourceText = QTextEdit(self.widget)
        self.selectSourceText.setObjectName(u"selectSourceText")
        self.selectSourceText.setGeometry(QRect(80, 350, 421, 41))
        self.urlLineEdit = QLineEdit(self.widget)
        self.urlLineEdit.setObjectName(u"urlLineEdit")
        self.urlLineEdit.setGeometry(QRect(80, 115, 501, 20))
        self.deleteButton = QPushButton(self.widget)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setGeometry(QRect(240, 615, 121, 24))
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(150, 295, 54, 20))
        self.selectTargetText = QTextEdit(self.widget)
        self.selectTargetText.setObjectName(u"selectTargetText")
        self.selectTargetText.setGeometry(QRect(80, 455, 421, 41))
        self.label_15 = QLabel(self.widget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(20, 10, 141, 16))
        self.selectTargetBtn = QPushButton(self.widget)
        self.selectTargetBtn.setObjectName(u"selectTargetBtn")
        self.selectTargetBtn.setGeometry(QRect(500, 455, 81, 41))
        self.secretCheckBox = QCheckBox(self.widget)
        self.secretCheckBox.setObjectName(u"secretCheckBox")
        self.secretCheckBox.setGeometry(QRect(210, 165, 191, 20))
        self.selectSourceBtn = QPushButton(self.widget)
        self.selectSourceBtn.setObjectName(u"selectSourceBtn")
        self.selectSourceBtn.setGeometry(QRect(500, 350, 81, 41))
        self.renameTargetLineEdit = QLineEdit(self.widget)
        self.renameTargetLineEdit.setObjectName(u"renameTargetLineEdit")
        self.renameTargetLineEdit.setGeometry(QRect(210, 510, 371, 20))
        self.saveButton = QPushButton(self.widget)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setGeometry(QRect(240, 575, 121, 24))
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 115, 51, 21))
        self.renameScriptLineEdit = QLineEdit(self.widget)
        self.renameScriptLineEdit.setObjectName(u"renameScriptLineEdit")
        self.renameScriptLineEdit.setGeometry(QRect(210, 295, 371, 20))
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 245, 31, 31))
        self.label_3.setWordWrap(True)
        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 355, 41, 31))
        self.label_5.setWordWrap(True)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 65, 51, 21))

        self.gridLayout.addWidget(self.widget, 0, 0, 5, 1)

        self.logTextEdit = QTextEdit(CustomDialog)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.logTextEdit, 4, 1, 1, 1)

        self.widget_2 = QWidget(CustomDialog)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(550, 330))
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.keyEdit = QLineEdit(self.widget_2)
        self.keyEdit.setObjectName(u"keyEdit")

        self.gridLayout_2.addWidget(self.keyEdit, 2, 1, 1, 6)

        self.label_12 = QLabel(self.widget_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)

        self.label_13 = QLabel(self.widget_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 5, 0, 1, 1)

        self.secretEdit = QLineEdit(self.widget_2)
        self.secretEdit.setObjectName(u"secretEdit")

        self.gridLayout_2.addWidget(self.secretEdit, 3, 1, 1, 6)

        self.targetComboBox = QComboBox(self.widget_2)
        self.targetComboBox.setObjectName(u"targetComboBox")

        self.gridLayout_2.addWidget(self.targetComboBox, 4, 1, 1, 6)

        self.sourceComboBox = QComboBox(self.widget_2)
        self.sourceComboBox.setObjectName(u"sourceComboBox")

        self.gridLayout_2.addWidget(self.sourceComboBox, 5, 1, 1, 6)

        self.label_11 = QLabel(self.widget_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_9 = QLabel(self.widget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_10 = QLabel(self.widget_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 0))
        self.label_10.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.label_10, 0, 0, 1, 3)

        self.detailLabel = QLabel(self.widget_2)
        self.detailLabel.setObjectName(u"detailLabel")
        font = QFont()
        font.setUnderline(True)
        self.detailLabel.setFont(font)

        self.gridLayout_2.addWidget(self.detailLabel, 0, 6, 1, 1)

        self.engineComboBox = QComboBox(self.widget_2)
        self.engineComboBox.setObjectName(u"engineComboBox")
        self.engineComboBox.setMinimumSize(QSize(260, 0))

        self.gridLayout_2.addWidget(self.engineComboBox, 0, 3, 1, 1)

        self.label_14 = QLabel(self.widget_2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 7, 0, 1, 1)

        self.untranslatedEdit = QLineEdit(self.widget_2)
        self.untranslatedEdit.setObjectName(u"untranslatedEdit")
        self.untranslatedEdit.setMinimumSize(QSize(0, 0))

        self.gridLayout_2.addWidget(self.untranslatedEdit, 7, 1, 1, 6)

        self.testButton = QPushButton(self.widget_2)
        self.testButton.setObjectName(u"testButton")

        self.gridLayout_2.addWidget(self.testButton, 8, 3, 1, 1)


        self.gridLayout.addWidget(self.widget_2, 2, 1, 1, 1)


        self.retranslateUi(CustomDialog)

        QMetaObject.connectSlotsByName(CustomDialog)
    # setupUi

    def retranslateUi(self, CustomDialog):
        CustomDialog.setWindowTitle(QCoreApplication.translate("CustomDialog", u"Custom Translation Engine", None))
        self.clearLogBtn.setText(QCoreApplication.translate("CustomDialog", u"clear log", None))
        self.selectScriptBtn.setText(QCoreApplication.translate("CustomDialog", u"...", None))
        self.label_8.setText(QCoreApplication.translate("CustomDialog", u"rename", None))
        self.nameLineEdit.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"relative to Active Translation Engine", None))
        self.renameScriptCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Rename Script", None))
        self.label_6.setText(QCoreApplication.translate("CustomDialog", u"rename", None))
        self.renameSourceLineEdit.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"rename the  source name in  'supported_language' folder", None))
        self.saveKeySecretCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Save the key and secret in the upper right corner", None))
#if QT_CONFIG(tooltip)
        self.selectScriptText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectScriptText.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"input or choose or drag the python script which supports translation api.  The script will be copied to 'custom_engine' folder", None))
        self.renameSourceCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Rename Source", None))
        self.renameTargetCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Rename Target", None))
        self.keyCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Key Support(API_KEY)", None))
        self.queueCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Queue Support (Can the api support list input in one request such as:['Hello','World'])", None))
        self.label_7.setText(QCoreApplication.translate("CustomDialog", u"target", None))
#if QT_CONFIG(tooltip)
        self.selectSourceText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectSourceText.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"input or choose or drag the source language file which applies language map.  The file will be copied to 'supported_language' folder", None))
        self.urlLineEdit.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"relative to detail information", None))
        self.deleteButton.setText(QCoreApplication.translate("CustomDialog", u"Delete", None))
        self.label_4.setText(QCoreApplication.translate("CustomDialog", u"rename", None))
#if QT_CONFIG(tooltip)
        self.selectTargetText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectTargetText.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"input or choose or drag the target language file which applies language map.  The file will be copied to 'supported_language' folder", None))
        self.label_15.setText(QCoreApplication.translate("CustomDialog", u"custom engine list", None))
        self.selectTargetBtn.setText(QCoreApplication.translate("CustomDialog", u"...", None))
        self.secretCheckBox.setText(QCoreApplication.translate("CustomDialog", u"Secret Support(API_SECRET)", None))
        self.selectSourceBtn.setText(QCoreApplication.translate("CustomDialog", u"...", None))
        self.renameTargetLineEdit.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"rename the  source name in  'supported_language' folder", None))
        self.saveButton.setText(QCoreApplication.translate("CustomDialog", u"Save", None))
        self.label_2.setText(QCoreApplication.translate("CustomDialog", u"url", None))
        self.renameScriptLineEdit.setPlaceholderText(QCoreApplication.translate("CustomDialog", u"rename the  script name in  'custom engine' folder", None))
        self.label_3.setText(QCoreApplication.translate("CustomDialog", u"script", None))
        self.label_5.setText(QCoreApplication.translate("CustomDialog", u"source", None))
        self.label.setText(QCoreApplication.translate("CustomDialog", u"name", None))
        self.label_12.setText(QCoreApplication.translate("CustomDialog", u"target", None))
        self.label_13.setText(QCoreApplication.translate("CustomDialog", u"source", None))
        self.secretEdit.setText("")
        self.label_11.setText(QCoreApplication.translate("CustomDialog", u"API_KEY:", None))
        self.label_9.setText(QCoreApplication.translate("CustomDialog", u"APP_SECRET:", None))
        self.label_10.setText(QCoreApplication.translate("CustomDialog", u"Active Translation Engine:", None))
        self.detailLabel.setText(QCoreApplication.translate("CustomDialog", u"detail information", None))
        self.label_14.setText(QCoreApplication.translate("CustomDialog", u"untranslated text", None))
        self.untranslatedEdit.setText("")
        self.testButton.setText(QCoreApplication.translate("CustomDialog", u"Test", None))
    # retranslateUi

