# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1411, 688)
        self.actioncopyright = QAction(MainWindow)
        self.actioncopyright.setObjectName(u"actioncopyright")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(750, 30, 711, 511))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.log_text = QTextEdit(self.centralwidget)
        self.log_text.setObjectName(u"log_text")
        self.log_text.setGeometry(QRect(580, 35, 821, 591))
        self.log_text.setReadOnly(True)
        self.clearLogBtn = QPushButton(self.centralwidget)
        self.clearLogBtn.setObjectName(u"clearLogBtn")
        self.clearLogBtn.setGeometry(QRect(960, 5, 75, 24))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 571, 341))
        self.translateBtn = QPushButton(self.widget)
        self.translateBtn.setObjectName(u"translateBtn")
        self.translateBtn.setGeometry(QRect(240, 310, 75, 24))
        self.selectFilesBtn = QPushButton(self.widget)
        self.selectFilesBtn.setObjectName(u"selectFilesBtn")
        self.selectFilesBtn.setGeometry(QRect(480, 25, 81, 41))
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 102, 61, 31))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 31, 31))
        self.label.setWordWrap(True)
        self.selectFilesText = QTextEdit(self.widget)
        self.selectFilesText.setObjectName(u"selectFilesText")
        self.selectFilesText.setGeometry(QRect(70, 25, 411, 41))
        self.selectDirBtn = QPushButton(self.widget)
        self.selectDirBtn.setObjectName(u"selectDirBtn")
        self.selectDirBtn.setGeometry(QRect(480, 100, 81, 41))
        self.selectDirText = QTextEdit(self.widget)
        self.selectDirText.setObjectName(u"selectDirText")
        self.selectDirText.setGeometry(QRect(70, 100, 411, 41))
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(250, 0, 60, 20))
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 170, 30, 31))
        self.selectFontText = QTextEdit(self.widget)
        self.selectFontText.setObjectName(u"selectFontText")
        self.selectFontText.setGeometry(QRect(70, 170, 411, 41))
        self.selectFontBtn = QPushButton(self.widget)
        self.selectFontBtn.setObjectName(u"selectFontBtn")
        self.selectFontBtn.setGeometry(QRect(480, 170, 81, 41))
        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 230, 41, 31))
        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(20, 275, 41, 31))
        self.targetComboBox = QComboBox(self.widget)
        self.targetComboBox.setObjectName(u"targetComboBox")
        self.targetComboBox.setGeometry(QRect(70, 235, 491, 22))
        self.sourceComboBox = QComboBox(self.widget)
        self.sourceComboBox.setObjectName(u"sourceComboBox")
        self.sourceComboBox.setGeometry(QRect(70, 280, 491, 22))
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(10, 360, 571, 271))
        self.selectFilesText_2 = QTextEdit(self.widget_2)
        self.selectFilesText_2.setObjectName(u"selectFilesText_2")
        self.selectFilesText_2.setGeometry(QRect(70, 40, 411, 41))
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 45, 31, 31))
        self.label_5.setWordWrap(True)
        self.selectFilesBtn_2 = QPushButton(self.widget_2)
        self.selectFilesBtn_2.setObjectName(u"selectFilesBtn_2")
        self.selectFilesBtn_2.setGeometry(QRect(480, 40, 81, 41))
        self.label_6 = QLabel(self.widget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(250, 10, 60, 20))
        self.selectDirBtn_2 = QPushButton(self.widget_2)
        self.selectDirBtn_2.setObjectName(u"selectDirBtn_2")
        self.selectDirBtn_2.setGeometry(QRect(480, 110, 81, 41))
        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 115, 61, 31))
        self.selectDirText_2 = QTextEdit(self.widget_2)
        self.selectDirText_2.setObjectName(u"selectDirText_2")
        self.selectDirText_2.setGeometry(QRect(70, 110, 411, 41))
        self.extractBtn = QPushButton(self.widget_2)
        self.extractBtn.setObjectName(u"extractBtn")
        self.extractBtn.setGeometry(QRect(240, 240, 75, 24))
        self.label_8 = QLabel(self.widget_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 185, 61, 31))
        self.tlNameText = QTextEdit(self.widget_2)
        self.tlNameText.setObjectName(u"tlNameText")
        self.tlNameText.setGeometry(QRect(70, 180, 491, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1411, 22))
        self.aboutMenu = QMenu(self.menubar)
        self.aboutMenu.setObjectName(u"aboutMenu")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.aboutMenu.menuAction())
        self.aboutMenu.addAction(self.actioncopyright)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ren'py Translator", None))
        self.actioncopyright.setText(QCoreApplication.translate("MainWindow", u"copyright", None))
        self.clearLogBtn.setText(QCoreApplication.translate("MainWindow", u"clear log", None))
        self.translateBtn.setText(QCoreApplication.translate("MainWindow", u"translate", None))
        self.selectFilesBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"directory", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"file(s)", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"input or choose or drag the file(s) you want to translate here. Examaple : F:\\GameName\\game\\tl\\language\\script.rpy", None))
        self.selectDirBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.selectDirText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"input or choose or drag the directory you want translate here.  Example:F:\\GameName\\game\\tl\\language", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"translation", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"font", None))
        self.selectFontText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"input or choose or drag the font which supports the language after translation. Example : DejaVuSans.ttf (ren'py 's default font)", None))
        self.selectFontBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"target", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"source", None))
#if QT_CONFIG(tooltip)
        self.selectFilesText_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFilesText_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"input or choose or drag the file(s) you want to extract here.    Examaple : F:\\GameName\\game\\script.rpy", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"file(s)", None))
        self.selectFilesBtn_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"extraction", None))
        self.selectDirBtn_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"directory", None))
        self.selectDirText_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"input or choose or drag the directory you want translate here.  Example:F:\\GameName\\game\\tl\\language", None))
        self.extractBtn.setText(QCoreApplication.translate("MainWindow", u"extract", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"tl name", None))
        self.tlNameText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"only needs in file(s) mode,if you input the directory , just fill nothing.                   input the directory name under game\\tl  Example: japanese or chinese  or  german", None))
        self.aboutMenu.setTitle(QCoreApplication.translate("MainWindow", u"about", None))
    # retranslateUi

