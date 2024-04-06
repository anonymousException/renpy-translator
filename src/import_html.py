# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_html.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_ImportHtmlDialog(object):
    def setupUi(self, ImportHtmlDialog):
        if not ImportHtmlDialog.objectName():
            ImportHtmlDialog.setObjectName(u"ImportHtmlDialog")
        ImportHtmlDialog.resize(652, 369)
        self.selecHtmlFileText = QTextEdit(ImportHtmlDialog)
        self.selecHtmlFileText.setObjectName(u"selecHtmlFileText")
        self.selecHtmlFileText.setGeometry(QRect(120, 30, 411, 91))
        self.selectHtmlFileBtn = QPushButton(ImportHtmlDialog)
        self.selectHtmlFileBtn.setObjectName(u"selectHtmlFileBtn")
        self.selectHtmlFileBtn.setGeometry(QRect(530, 30, 81, 91))
        self.selectHtmlFileBtn.setText(u"...")
        self.label = QLabel(ImportHtmlDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 45, 101, 71))
        self.label.setWordWrap(True)
        self.selectTranslatedFileText = QTextEdit(ImportHtmlDialog)
        self.selectTranslatedFileText.setObjectName(u"selectTranslatedFileText")
        self.selectTranslatedFileText.setGeometry(QRect(120, 170, 411, 91))
        self.selectTranslatedFileBtn = QPushButton(ImportHtmlDialog)
        self.selectTranslatedFileBtn.setObjectName(u"selectTranslatedFileBtn")
        self.selectTranslatedFileBtn.setGeometry(QRect(530, 170, 81, 91))
        self.selectTranslatedFileBtn.setText(u"...")
        self.label_2 = QLabel(ImportHtmlDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 185, 101, 71))
        self.label_2.setWordWrap(True)
        self.importBtn = QPushButton(ImportHtmlDialog)
        self.importBtn.setObjectName(u"importBtn")
        self.importBtn.setGeometry(QRect(90, 310, 491, 24))

        self.retranslateUi(ImportHtmlDialog)

        QMetaObject.connectSlotsByName(ImportHtmlDialog)
    # setupUi

    def retranslateUi(self, ImportHtmlDialog):
        ImportHtmlDialog.setWindowTitle(QCoreApplication.translate("ImportHtmlDialog", u"Import html and relative translated contents", None))
#if QT_CONFIG(tooltip)
        self.selecHtmlFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selecHtmlFileText.setPlaceholderText(QCoreApplication.translate("ImportHtmlDialog", u"input or choose or drag the html file exported before.Example:F:/exported.html", None))
        self.label.setText(QCoreApplication.translate("ImportHtmlDialog", u"html file", None))
#if QT_CONFIG(tooltip)
        self.selectTranslatedFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectTranslatedFileText.setPlaceholderText(QCoreApplication.translate("ImportHtmlDialog", u"input or choose or drag the relative translated file.Example:F:/translated.txt", None))
        self.label_2.setText(QCoreApplication.translate("ImportHtmlDialog", u"translated file", None))
        self.importBtn.setText(QCoreApplication.translate("ImportHtmlDialog", u"Import Files", None))
    # retranslateUi

