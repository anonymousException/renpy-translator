import io
import os.path
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialog, QFileDialog

from my_log import log_print
from default_language import Ui_DefaultLanguageDialog

default_language_template_path = 'default_langauge_template.txt'
out_default_lanugage_script_name = 'set_default_language_at_startup.rpy'


def set_default_language_at_startup(tl_name, target):
    f = io.open(default_language_template_path, 'r', encoding='utf-8')
    _data = f.read()
    f.close()
    _data = _data.replace('{tl_name}', tl_name)
    f = io.open(target, 'w', encoding='utf-8')
    f.write(_data)
    f.close()
    log_print(f'set default langauge to {tl_name} success!')


class MyDefaultLanguageForm(QDialog, Ui_DefaultLanguageDialog):
    def __init__(self, parent=None):
        super(MyDefaultLanguageForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.selectFileText.textChanged.connect(self.on_text_changed)
        self.tlNameText.textChanged.connect(self.on_tl_name_changed)
        self.setDefaultLanguageCheckBox.clicked.connect(self.on_default_language_checkbox_clicked)

    def on_tl_name_changed(self):
        target = self.get_target()
        if target is not None and os.path.isfile(target):
            f = io.open(target, 'r', encoding='utf-8')
            _lines = f.readlines()
            f.close()
            tl_name = ''
            for index, _line in enumerate(_lines):
                if 'renpy.game.preferences.language' in _line:
                    idx = _line.rindex('=')
                    tl_name = _line[idx + 1:].strip().strip('"')
                    _lines[index] = _lines[index].replace(tl_name, self.tlNameText.toPlainText())
                    break
            f = io.open(target, 'w', encoding='utf-8')
            f.writelines(_lines)
            f.close()
            self.setDefaultLanguageCheckBox.setChecked(True)
        else:
            self.setDefaultLanguageCheckBox.setChecked(False)

    def on_default_language_checkbox_clicked(self):
        tl_name = self.tlNameText.toPlainText()
        if self.setDefaultLanguageCheckBox.isChecked():
            target = self.get_target()
            if target is not None:
                set_default_language_at_startup(tl_name, target)
        else:
            target = self.get_target()
            if target is not None:
                if os.path.isfile(target):
                    os.remove(target)
                if os.path.isfile(target + 'c'):
                    os.remove(target + 'c')
                log_print('remove set default langauge success!')

    def get_target(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                target = os.path.dirname(path)
                target = target + '/game'
                if os.path.isdir(target):
                    target = target + '/' + out_default_lanugage_script_name
                    return target
        return None

    def on_text_changed(self):
        target = self.get_target()
        if target is not None and os.path.isfile(target):
            f = io.open(target, 'r', encoding='utf-8')
            _lines = f.readlines()
            f.close()
            tl_name = ''
            for _line in _lines:
                if 'renpy.game.preferences.language' in _line:
                    idx = _line.rindex('=')
                    tl_name = _line[idx + 1:].strip().strip('"')
                    break
            self.setDefaultLanguageCheckBox.setChecked(True)
            self.tlNameText.setText(tl_name)
        else:
            self.setDefaultLanguageCheckBox.setChecked(False)

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('DefaultLanguageDialog',
                                                                                'select the game file you want to set default language at startup',
                                                                                None),
                                                     '',
                                                     "Game Files (*.exe)")
        self.selectFileText.setText(file)
