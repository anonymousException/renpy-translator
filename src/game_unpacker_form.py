import _thread
import io
import os
import shutil
import subprocess
import threading
import time
import traceback

import win32con
import win32gui
from PySide6.QtCore import QThread, Signal, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from my_log import log_print
import my_log
from renpy_fonts import GenGuiFonts
from game_unpacker import Ui_GameUnpackerDialog

bat = 'UnRen-forall.bat'
hook_script = 'hook_unrpa.rpy'
finish_flag = '/unpack.finish'
expand_file = 'expand.exe'


def set_window_on_top(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)
    except:
        pass


class unrpycThread(threading.Thread):
    def __init__(self, dir, p, is_auto_close):
        threading.Thread.__init__(self)
        self.dir = dir
        self.p = p
        self.is_auto_close = is_auto_close

    def run(self):
        try:
            if self.is_auto_close:
                self.p.kill()
            dir = self.dir
            bat = os.getcwd() + '/UnRen-forall.bat'
            command = bat
            p = subprocess.Popen(command, shell=False, stdout=my_log.f, stderr=my_log.f,
                                 creationflags=0x08000000, text=True, cwd=dir, encoding='utf-8')
            p.wait()
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


class MyGameUnpackerForm(QDialog, Ui_GameUnpackerDialog):
    def __init__(self, parent=None):
        super(MyGameUnpackerForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('main.ico'))
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.unpackBtn.clicked.connect(self.unpack)
        self.hwnd = win32gui.GetForegroundWindow()
        self.parent_hwnd = None
        self.path = None
        self.p = None
        self.dir = None
        _thread.start_new_thread(self.update, ())

    def closeEvent(self, event):
        self.parent.widget.show()
        self.parent.menubar.show()
        self.parent.versionLabel.show()
        self.parent.actionunpack_game.triggered.connect(lambda: self.parent.unpack_game())
        self.parent.showNormal()
        self.hide()
        event.ignore()
        return

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('GameUnpackerDialog',
                                                                                'select the game file you want to unpack',
                                                                                None),
                                                     '',
                                                     "Game Files (*.exe)")
        self.selectFileText.setText(file)

    def unpack(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                shutil.copyfile(hook_script, dir + '/game/' + hook_script)
                command = path
                self.path = path
                f = io.open(dir + finish_flag, 'w')
                f.write('waiting')
                f.close()
                self.setDisabled(True)
                log_print('start unpacking...')
                p = subprocess.Popen(command, shell=False, stdout=my_log.f, stderr=my_log.f,
                                     creationflags=0x08000000, text=True, cwd=dir, encoding='utf-8')
                self.p = p
                self.hwnd = win32gui.GetForegroundWindow()
                self.hide()
                self.parent.showNormal()
                self.parent.raise_()
                self.parent_hwnd = win32gui.GetForegroundWindow()

    def update(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self):
        try:
            if self.p is not None:
                if self.p.poll() is not None:
                    self.p = None
            if self.dir is not None:
                if os.path.isfile(self.dir + '/unren.finish'):
                    os.remove(self.dir + '/unren.finish')
                    self.show()
                    self.raise_()
                    set_window_on_top(self.hwnd)
                    self.dir = None
                    self.setEnabled(True)
                    log_print('unpack complete!')
            if self.path is None:
                return
            dir = os.path.dirname(self.path)
            target = dir + finish_flag
            if not os.path.isfile(target):
                hook_script_path = dir + '/game/' + hook_script
                if os.path.isfile(hook_script_path):
                    os.remove(hook_script_path)
                if os.path.isfile(hook_script_path + 'c'):
                    os.remove(hook_script_path + 'c')
                set_window_on_top(self.parent_hwnd)
                t = unrpycThread(dir, self.p, self.autoCheckBox.isChecked())
                t.start()
                self.path = None
                self.dir = dir
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
