# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pack_game.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QLabel, QListView, QPushButton, QSizePolicy,
    QTextEdit, QWidget)

class Ui_PackGameDialog(object):
    def setupUi(self, PackGameDialog):
        if not PackGameDialog.objectName():
            PackGameDialog.setObjectName(u"PackGameDialog")
        PackGameDialog.resize(1082, 592)
        self.gridLayout = QGridLayout(PackGameDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(PackGameDialog)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(600, 410))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 71, 61))
        self.label.setWordWrap(True)
        self.selectDirsBtn = QPushButton(self.widget)
        self.selectDirsBtn.setObjectName(u"selectDirsBtn")
        self.selectDirsBtn.setGeometry(QRect(500, 320, 81, 81))
        self.selectDirsBtn.setText(u"...")
        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 330, 81, 31))
        self.label_13.setWordWrap(True)
        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 235, 71, 31))
        self.label_5.setWordWrap(True)
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 130, 61, 61))
        self.label_8.setWordWrap(True)
        self.selectFilesBtn = QPushButton(self.widget)
        self.selectFilesBtn.setObjectName(u"selectFilesBtn")
        self.selectFilesBtn.setGeometry(QRect(500, 220, 81, 81))
        self.selectFilesBtn.setText(u"...")
        self.selectDirsText = QTextEdit(self.widget)
        self.selectDirsText.setObjectName(u"selectDirsText")
        self.selectDirsText.setGeometry(QRect(90, 320, 411, 81))
        self.selectFileBtn = QPushButton(self.widget)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(500, 5, 81, 91))
        self.selectFileBtn.setText(u"...")
        self.selectFileText = QTextEdit(self.widget)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(90, 5, 411, 91))
        self.packageNameText = QTextEdit(self.widget)
        self.packageNameText.setObjectName(u"packageNameText")
        self.packageNameText.setGeometry(QRect(90, 120, 491, 81))
        self.selectFilesText = QTextEdit(self.widget)
        self.selectFilesText.setObjectName(u"selectFilesText")
        self.selectFilesText.setGeometry(QRect(90, 220, 411, 81))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.listView = QListView(PackGameDialog)
        self.listView.setObjectName(u"listView")

        self.gridLayout.addWidget(self.listView, 0, 1, 5, 1)

        self.appendButton = QPushButton(PackGameDialog)
        self.appendButton.setObjectName(u"appendButton")

        self.gridLayout.addWidget(self.appendButton, 1, 0, 1, 1)

        self.autoCopyTranslationCheckBox = QCheckBox(PackGameDialog)
        self.autoCopyTranslationCheckBox.setObjectName(u"autoCopyTranslationCheckBox")
        self.autoCopyTranslationCheckBox.setMinimumSize(QSize(0, 50))
        self.autoCopyTranslationCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.autoCopyTranslationCheckBox, 2, 0, 1, 1)

        self.autoCopyFontCheckBox = QCheckBox(PackGameDialog)
        self.autoCopyFontCheckBox.setObjectName(u"autoCopyFontCheckBox")
        self.autoCopyFontCheckBox.setMinimumSize(QSize(0, 50))
        self.autoCopyFontCheckBox.setChecked(True)

        self.gridLayout.addWidget(self.autoCopyFontCheckBox, 3, 0, 1, 1)

        self.packBtn = QPushButton(PackGameDialog)
        self.packBtn.setObjectName(u"packBtn")

        self.gridLayout.addWidget(self.packBtn, 4, 0, 1, 1)


        self.retranslateUi(PackGameDialog)

        QMetaObject.connectSlotsByName(PackGameDialog)
    # setupUi

    def retranslateUi(self, PackGameDialog):
        PackGameDialog.setWindowTitle(QCoreApplication.translate("PackGameDialog", u"Pack game files into rpa package", None))
        self.label.setText(QCoreApplication.translate("PackGameDialog", u"file", None))
        self.label_13.setText(QCoreApplication.translate("PackGameDialog", u"directory(s)", None))
        self.label_5.setText(QCoreApplication.translate("PackGameDialog", u"file(s)", None))
        self.label_8.setText(QCoreApplication.translate("PackGameDialog", u"name", None))
#if QT_CONFIG(tooltip)
        self.selectDirsText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectDirsText.setPlaceholderText(QCoreApplication.translate("PackGameDialog", u"input or choose or drag the directory(s) you want to pack here.Examaple:D:\\GameName\\game\\character", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("PackGameDialog", u"input or choose or drag the game you want to pack it's files.Example:F:/DemoGame.exe", None))
        self.packageNameText.setPlaceholderText(QCoreApplication.translate("PackGameDialog", u"input the rpa name as your wish , if the file already exists under game folder , the files will be appened into it", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText.setPlaceholderText(QCoreApplication.translate("PackGameDialog", u"input or choose or drag the file(s) you want to pack here.Examaple:D:\\GameName\\game\\script.rpy", None))
        self.appendButton.setText(QCoreApplication.translate("PackGameDialog", u"Append to file list", None))
        self.autoCopyTranslationCheckBox.setText(QCoreApplication.translate("PackGameDialog", u"Auto append translation files", None))
        self.autoCopyFontCheckBox.setText(QCoreApplication.translate("PackGameDialog", u"Auto append font files", None))
        self.packBtn.setText(QCoreApplication.translate("PackGameDialog", u"pack game files", None))
    # retranslateUi

