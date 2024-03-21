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
        LocalGlossaryDialog.resize(731, 552)
        self.gridLayout = QGridLayout(LocalGlossaryDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectFileText = QTextEdit(LocalGlossaryDialog)
        self.selectFileText.setObjectName(u"selectFileText")
        self.selectFileText.setMinimumSize(QSize(0, 40))
        self.selectFileText.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.selectFileText, 0, 1, 1, 1)

        self.duplicateCheckBox = QCheckBox(LocalGlossaryDialog)
        self.duplicateCheckBox.setObjectName(u"duplicateCheckBox")

        self.gridLayout.addWidget(self.duplicateCheckBox, 1, 1, 1, 1)

        self.label = QLabel(LocalGlossaryDialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(30, 30))
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.confirmButton = QPushButton(LocalGlossaryDialog)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMaximumSize(QSize(16777215, 24))

        self.gridLayout.addWidget(self.confirmButton, 4, 0, 1, 4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 4)

        self.appendCheckBox = QCheckBox(LocalGlossaryDialog)
        self.appendCheckBox.setObjectName(u"appendCheckBox")
        self.appendCheckBox.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.appendCheckBox, 0, 3, 1, 1)

        self.selectFileBtn = QPushButton(LocalGlossaryDialog)
        self.selectFileBtn.setObjectName(u"selectFileBtn")
        self.selectFileBtn.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.selectFileBtn, 0, 2, 1, 1)

        self.label_2 = QLabel(LocalGlossaryDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 3)


        self.retranslateUi(LocalGlossaryDialog)

        QMetaObject.connectSlotsByName(LocalGlossaryDialog)
    # setupUi

    def retranslateUi(self, LocalGlossaryDialog):
        LocalGlossaryDialog.setWindowTitle(QCoreApplication.translate("LocalGlossaryDialog", u"Local Glossary", None))
#if QT_CONFIG(tooltip)
        self.selectFileText.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.selectFileText.setPlaceholderText(QCoreApplication.translate("LocalGlossaryDialog", u"input or choose or drag the file(s) you want to edit here. Examaple : F:\\xxx.xslx", None))
        self.duplicateCheckBox.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Show duplicate rows only (if duplicated, only the last one will take effect)", None))
        self.label.setText(QCoreApplication.translate("LocalGlossaryDialog", u"file", None))
        self.confirmButton.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Confirm", None))
        self.appendCheckBox.setText(QCoreApplication.translate("LocalGlossaryDialog", u"Support Append", None))
        self.selectFileBtn.setText(QCoreApplication.translate("LocalGlossaryDialog", u"...", None))
        self.label_2.setText(QCoreApplication.translate("LocalGlossaryDialog", u"For more advanced editing functions, it is recommended to use professional software such as Excel.", None))
    # retranslateUi

