import io
import json
import os
import webbrowser

from PySide6 import QtCore
from PySide6.QtWidgets import QDialog

from engine import Ui_EngineDialog
from my_log import log_print
from renpy_translate import engineDic, engineList


class MyEngineForm(QDialog, Ui_EngineDialog):
    def __init__(self, parent=None):
        super(MyEngineForm, self).__init__(parent)
        self.setupUi(self)
        self.detailLabel.setStyleSheet(
            "QLabel::hover"
            "{"
            "background-color : lightgreen;"
            "}"
        )
        self.detailLabel.setStyleSheet("color:blue")
        self.setFixedHeight(200)
        for i in engineDic.keys():
            self.engineComboBox.addItem(i)
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            customEngineDic = json.load(f)
            f.close()
            for i in customEngineDic.keys():
                self.engineComboBox.addItem(i)
        self.init_openai_model_combobox()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                self.engineComboBox.setCurrentIndex(self.engineComboBox.findText(loaded_data['engine']))
                self.keyEdit.setText(loaded_data['key'])
                self.secretEdit.setText((loaded_data['secret']))
                if "rpm" in loaded_data:
                    self.rpmEdit.setText(loaded_data['rpm'])
                if "rps" in loaded_data:
                    self.rpsEdit.setText(loaded_data['rps'])
                if "tpm" in loaded_data:
                    self.tpmEdit.setText(loaded_data['tpm'])
                if "openai_model_index" in loaded_data:
                    self.modelComboBox.setCurrentIndex(loaded_data['openai_model_index'])
                if "openai_base_url" in loaded_data:
                    self.baseUrlEdit.setText(loaded_data['openai_base_url'])
            self.init_edit_status()
            if self.engineComboBox.currentText() == engineList[4]:
                self.setFixedHeight(300)
        else:
            self.engineComboBox.setCurrentIndex(0)
            self.on_combobox_change()
        self.confirmButton.clicked.connect(self.confirm)
        self.engineComboBox.currentIndexChanged.connect(self.on_combobox_change)
        self.detailLabel.mousePressEvent = self.open_url
        self.detailLabel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.customButton.clicked.connect(self.on_custom_button_clicked)

    def on_custom_button_clicked(self):
        if os.path.isfile('openai_model.txt'):
            os.system('notepad ' + 'openai_model.txt')
            self.init_openai_model_combobox()

    def init_edit_status(self):
        customEngineDic = dict()
        current_text = self.engineComboBox.currentText()
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            customEngineDic = json.load(f)
            f.close()
        if current_text in engineDic.keys():
            if engineDic[current_text]['key_edit']:
                self.keyEdit.setEnabled(True)
            else:
                self.keyEdit.setDisabled(True)

            if engineDic[current_text]['secret_edit']:
                self.secretEdit.setEnabled(True)
            else:
                self.secretEdit.setDisabled(True)
        elif current_text in customEngineDic.keys():
            if customEngineDic[current_text]['key_edit']:
                self.keyEdit.setEnabled(True)
            else:
                self.keyEdit.setDisabled(True)
            if customEngineDic[current_text]['secret_edit']:
                self.secretEdit.setEnabled(True)
            else:
                self.secretEdit.setDisabled(True)
        else:
            log_print(current_text + 'not in dic error!')

    def init_openai_model_combobox(self):
        self.modelComboBox.clear()
        if os.path.isfile('openai_model.txt'):
            f = io.open('openai_model.txt', 'r',encoding='utf-8')
            models = f.readlines()
            f.close()
            for i in models:
                self.modelComboBox.addItem(i.rstrip('\n'))


    def open_url(self, event):
        current_text = self.engineComboBox.currentText()
        if current_text in engineDic.keys():
            webbrowser.open(engineDic[current_text]['url'])
        else:
            if os.path.isfile('custom.txt'):
                f = io.open('custom.txt', 'r', encoding='utf-8')
                customEngineDic = json.load(f)
                f.close()
                if current_text in customEngineDic.keys():
                    webbrowser.open(customEngineDic[current_text]['url'])

    def on_combobox_change(self):
        self.setFixedHeight(200)
        if self.engineComboBox.currentText() == engineList[4]:
            self.setFixedHeight(300)
        self.init_edit_status()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                key = str(self.engineComboBox.currentText()) + '_key'
                secret = str(self.engineComboBox.currentText()) + '_secret'
                if key in loaded_data:
                    self.keyEdit.setText(loaded_data[key])
                else:
                    self.keyEdit.setText('')
                if secret in loaded_data:
                    self.secretEdit.setText(loaded_data[secret])
                else:
                    self.secretEdit.setText('')

    def confirm(self):
        if not os.path.isfile('engine.txt'):
            f = io.open('engine.txt', 'w', encoding='utf-8')
            data = {"engine": self.engineComboBox.currentText(), "key": self.keyEdit.text(),
                    "secret": self.secretEdit.text(),
                    str(self.engineComboBox.currentText()) + '_key': self.keyEdit.text(),
                    str(self.engineComboBox.currentText()) + '_secret': self.secretEdit.text(),
                    "rpm": self.rpmEdit.text(),
                    "rps": self.rpsEdit.text(),
                    "tpm": self.tpmEdit.text(),
                    "openai_model": self.modelComboBox.currentText(),
                    "openai_base_url": self.baseUrlEdit.text(),
                    "openai_model_index": self.modelComboBox.currentIndex()}
            json.dump(data, f)
            f.close()
        else:
            f = io.open('engine.txt', 'r', encoding='utf-8')
            loaded_data = json.load(f)
            f.close()
            f = io.open('engine.txt', 'w', encoding='utf-8')
            loaded_data['engine'] = self.engineComboBox.currentText()
            loaded_data['key'] = self.keyEdit.text()
            loaded_data['secret'] = self.secretEdit.text()
            loaded_data[str(self.engineComboBox.currentText()) + '_key'] = self.keyEdit.text()
            loaded_data[str(self.engineComboBox.currentText()) + '_secret'] = self.secretEdit.text()
            loaded_data['rpm'] = self.rpmEdit.text()
            loaded_data['rps'] = self.rpsEdit.text()
            loaded_data['tpm'] = self.tpmEdit.text()
            loaded_data['openai_model'] = self.modelComboBox.currentText()
            loaded_data['openai_base_url'] = self.baseUrlEdit.text()
            loaded_data['openai_model_index'] = self.modelComboBox.currentIndex()
            json.dump(loaded_data, f)
            f.close()
        self.close()