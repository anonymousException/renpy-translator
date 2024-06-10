# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'translated.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QPlainTextEdit,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_TranslatedDialog(object):
    def setupUi(self, TranslatedDialog):
        if not TranslatedDialog.objectName():
            TranslatedDialog.setObjectName(u"TranslatedDialog")
        TranslatedDialog.resize(612, 444)
        self.gridLayout = QGridLayout(TranslatedDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plainTextEdit = QPlainTextEdit(TranslatedDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(580, 250))

        self.gridLayout.addWidget(self.plainTextEdit, 1, 0, 1, 1)

        self.confirmButton = QPushButton(TranslatedDialog)
        self.confirmButton.setObjectName(u"confirmButton")

        self.gridLayout.addWidget(self.confirmButton, 2, 0, 1, 1)

        self.widget = QWidget(TranslatedDialog)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(580, 100))
        self.selectFileBtn = QPushButton(self.widget)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setGeometry(QRect(490, 10, 101, 81))
        self.selectFileBtn.setText(u"...")
        self.selectFileText = QTextEdit(self.widget)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setGeometry(QRect(0, 10, 491, 81))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(TranslatedDialog)

        QMetaObject.connectSlotsByName(TranslatedDialog)
    # setupUi

    def retranslateUi(self, TranslatedDialog):
        TranslatedDialog.setWindowTitle(QCoreApplication.translate("TranslatedDialog", u"Translate with translated contents", None))
        self.plainTextEdit.setPlaceholderText(QCoreApplication.translate("TranslatedDialog", u"you can also just directly paste the translated contents here", None))
        self.confirmButton.setText(QCoreApplication.translate("TranslatedDialog", u"Confirm", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("TranslatedDialog", u"input or choose or drag the file already translated. Examaple : F:\\translated.txt", None))
    # retranslateUi

