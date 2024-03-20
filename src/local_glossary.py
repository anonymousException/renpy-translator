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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_LocalGlossaryDialog(object):
    def setupUi(self, LocalGlossaryDialog):
        if not LocalGlossaryDialog.objectName():
            LocalGlossaryDialog.setObjectName(u"LocalGlossaryDialog")
        LocalGlossaryDialog.resize(705, 527)
        self.gridLayout = QGridLayout(LocalGlossaryDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.appendCheckBox = QCheckBox(LocalGlossaryDialog)
        self.appendCheckBox.setObjectName(u"appendCheckBox")
        self.appendCheckBox.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.appendCheckBox, 0, 3, 1, 1)

        self.label = QLabel(LocalGlossaryDialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(30, 30))
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 4)

        self.selectFileBtn = QPushButton(LocalGlossaryDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.selectFileBtn, 0, 2, 1, 1)

        self.selectFileText = QTextEdit(LocalGlossaryDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setMinimumSize(QSize(0, 40))
        self.selectFileText.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.selectFileText, 0, 1, 1, 1)

        self.confirmButton = QPushButton(LocalGlossaryDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMaximumSize(QSize(16777215, 24))

        self.gridLayout.addWidget(self.confirmButton, 2, 0, 1, 4)


        self.retranslateUi(LocalGlossaryDialog)

        QMetaObject.connectSlotsByName(LocalGlossaryDialog)
    # setupUi

    def retranslateUi(self, LocalGlossaryDialog):
        LocalGlossaryDialog.setWindowTitle(QCoreApplication.translate("LocalGlossaryDialog", u"Local Glossary", None))
        self.appendCheckBox.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Support Append", None))
        self.label.setText(QCoreApplication.translate("LocalGlossaryDialog", u"file", None))
        self.selectFileBtn.setText(QCoreApplication.translate("LocalGlossaryDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("LocalGlossaryDialog", u"input or choose or drag the file(s) you want to edit here. Examaple : F:\\xxx.xslx", None))
        self.confirmButton.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Confirm", None))
    # retranslateUi

