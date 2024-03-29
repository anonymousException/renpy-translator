import _thread
import io
import os
import shutil
import threading
import time
import traceback

from PySide6.QtCore import QThread, Signal, QCoreApplication
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from my_log import log_print
from renpy_fonts import GenGuiFonts
from game_unpacker import Ui_GameUnpackerDialog

bat = 'UnRen-forall.bat'
hook_script = 'hook_unrpa.rpy'
finish_flag = '/unpack.finish'
expand_file = 'expand.exe'

class MyGameUnpackerForm(QDialog, Ui_GameUnpackerDialog):
    def __init__(self, parent=None):
        super(MyGameUnpackerForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.unpackBtn.clicked.connect(self.unpack)
        self.cleanBtn.clicked.connect(lambda: self.clean(False))
        self.path = None
        _thread.start_new_thread(self.update, ())

    def closeEvent(self, event):
        self.path = None

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('GameUnpackerDialog', 'select the game file you want to unpack', None),
                                                     '',
                                                     "Game Files (*.exe)")
        self.selectFileText.setText(file)

    def unpack(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)

                shutil.copyfile(bat, dir + '/' + bat)
                shutil.copyfile(expand_file, dir + '/' + expand_file)

                shutil.copyfile(hook_script, dir + '/game/' + hook_script)
                command = 'start "" /d "' + dir + '"  "' + path + '"'
                self.path = path
                f = io.open(dir + finish_flag, 'w')
                f.write('waiting')
                f.close()
                self.setDisabled(True)
                os.system(command)

    def clean(self, is_auto_clean=False):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                hook_script_path = dir + '/game/' + hook_script
                if os.path.isfile(hook_script_path):
                    os.remove(hook_script_path)
                if os.path.isfile(hook_script_path + 'c'):
                    os.remove(hook_script_path + 'c')
                bat_path = dir + '/' + bat
                if os.path.isfile(bat_path):
                    os.remove(bat_path)
                expand_path = dir + '/' + expand_file
                if os.path.isfile(expand_path):
                    os.remove(expand_path)
                if not is_auto_clean:
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle('o(≧口≦)o')
                    msg_box.setText(QCoreApplication.translate('GameUnpackerDialog', 'Clean Complete', None))
                    msg_box.exec()

    def update(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self):
        try:
            if self.path is None:
                return
            dir = os.path.dirname(self.path)
            target = dir + finish_flag
            if not os.path.isfile(target):
                bat = dir + '/UnRen-forall.bat'
                command = 'start "" /d "' + dir + '"  "' + bat + '"'
                os.system(command)
                while (True):
                    time.sleep(0.1)
                    if os.path.isfile(dir + '/unren.finish'):
                        os.remove(dir + '/unren.finish')
                        break
                if self.autoCheckBox.isChecked():
                    self.clean(is_auto_clean = True)
                self.path = None
                self.setEnabled(True)
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)

    class UpdateThread(QThread):
        update_date = Signal()

        def __init__(self):
            super().__init__()

        def __del__(self):
            self.wait()

        def run(self):
            self.update_date.emit()