# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'local_glossary.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_LocalGlossaryDialog(object):
    def setupUi(self, LocalGlossaryDialog):
        if not LocalGlossaryDialog.objectName():
            LocalGlossaryDialog.setObjectName(u"LocalGlossaryDialog")
        LocalGlossaryDialog.resize(700, 567)
        self.gridLayout = QGridLayout(LocalGlossaryDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectFileText = QTextEdit(LocalGlossaryDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setMinimumSize(QSize(0, 60))
        self.selectFileText.setMaximumSize(QSize(16777215, 60))

        self.gridLayout.addWidget(self.selectFileText, 0, 1, 1, 1)

        self.confirmButton = QPushButton(LocalGlossaryDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMaximumSize(QSize(16777215, 24))
        self.confirmButton.setAutoDefault(False)

        self.gridLayout.addWidget(self.confirmButton, 9, 0, 1, 4)

        self.label = QLabel(LocalGlossaryDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(200, 20))
        self.label.setMaximumSize(QSize(100, 30))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.prevButton = QPushButton(LocalGlossaryDialog)
        self.prevButton.setObjectName(u"prevButton")
        self.prevButton.setMinimumSize(QSize(200, 0))
        self.prevButton.setMaximumSize(QSize(200, 16777215))
        self.prevButton.setAutoDefault(False)

        self.gridLayout.addWidget(self.prevButton, 7, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout.addLayout(self.verticalLayout, 8, 0, 1, 4)

        self.nextButton = QPushButton(LocalGlossaryDialog)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setMinimumSize(QSize(200, 0))
        self.nextButton.setMaximumSize(QSize(200, 16777215))
        self.nextButton.setAutoDefault(False)

        self.gridLayout.addWidget(self.nextButton, 7, 2, 1, 2)

        self.selectFileBtn = QPushButton(LocalGlossaryDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setMinimumSize(QSize(100, 60))
        self.selectFileBtn.setAutoDefault(False)

        self.gridLayout.addWidget(self.selectFileBtn, 0, 2, 1, 1)

        self.widget = QWidget(LocalGlossaryDialog)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(670, 120))
        self.widget.setMaximumSize(QSize(16777215, 80))
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(-2, 45, 351, 20))
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.pageRowsLineEdit = QLineEdit(self.widget)
        self.pageRowsLineEdit.setObjectName(u"pageRowsLineEdit")
        self.pageRowsLineEdit.setGeometry(QRect(350, 70, 281, 20))
        self.pageRowsLineEdit.setMaximumSize(QSize(16777215, 16777215))
        self.pageRowsLineEdit.setAlignment(Qt.AlignCenter)
        self.pageRowsLineEdit.setPlaceholderText(u"100")
        self.gotoPageLineEdit = QLineEdit(self.widget)
        self.gotoPageLineEdit.setObjectName(u"gotoPageLineEdit")
        self.gotoPageLineEdit.setGeometry(QRect(350, 45, 281, 20))
        self.gotoPageLineEdit.setAlignment(Qt.AlignCenter)
        self.gotoPageLineEdit.setPlaceholderText(u"1")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 70, 341, 20))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, -10, 651, 60))
        self.label_2.setMinimumSize(QSize(0, 60))
        self.label_2.setMaximumSize(QSize(16777215, 60))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.gotoPageButton = QPushButton(self.widget)
        self.gotoPageButton.setObjectName(u"gotoPageButton")
        self.gotoPageButton.setGeometry(QRect(630, 45, 41, 20))
        self.gotoPageButton.setText(u"\u221a")
        self.gotoPageButton.setAutoDefault(False)
        self.maxPageRowsButton = QPushButton(self.widget)
        self.maxPageRowsButton.setObjectName(u"maxPageRowsButton")
        self.maxPageRowsButton.setGeometry(QRect(630, 70, 41, 20))
        self.maxPageRowsButton.setText(u"\u221a")
        self.maxPageRowsButton.setAutoDefault(False)

        self.gridLayout.addWidget(self.widget, 2, 0, 1, 3)

        self.curPageLabel = QLabel(LocalGlossaryDialog)
        self.curPageLabel.setObjectName(u"curPageLabel")
        self.curPageLabel.setText(u"0/0")
        self.curPageLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.curPageLabel, 7, 1, 1, 1)


        self.retranslateUi(LocalGlossaryDialog)

        QMetaObject.connectSlotsByName(LocalGlossaryDialog)
    # setupUi

    def retranslateUi(self, LocalGlossaryDialog):
        LocalGlossaryDialog.setWindowTitle(QCoreApplication.translate("LocalGlossaryDialog", u"Local Glossary", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("LocalGlossaryDialog", u"input or choose or drag the file(s) you want to edit here. Examaple : F:\\xxx.xslx", None))
        self.confirmButton.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Confirm", None))
        self.label.setText(QCoreApplication.translate("LocalGlossaryDialog", u"file", None))
        self.prevButton.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Previous", None))
        self.nextButton.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Next", None))
        self.selectFileBtn.setText(QCoreApplication.translate("LocalGlossaryDialog", u"...", None))
        self.label_3.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Go to page", None))
        self.label_4.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Max Page Rows", None))
        self.label_2.setText(QCoreApplication.translate("LocalGlossaryDialog", u"For more advanced editing functions, it is recommended to use professional software such as Excel.", None))
    # retranslateUi

