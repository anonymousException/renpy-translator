import _thread
import os
import threading
import time
import traceback

from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog, QFileDialog

from error_repair import Ui_ErrorRepairDialog
from my_log import log_print
from renpy_lint import fix_translation_by_lint_recursion


class repairThread(threading.Thread):
    def __init__(self, path, max_recursion_depth):
        threading.Thread.__init__(self)
        self.path = path
        self.max_recursion_depth = max_recursion_depth

    def run(self):
        try:
            log_print('start repairing ...')
            fix_translation_by_lint_recursion(self.path, self.max_recursion_depth)
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


class MyErrorRepairForm(QDialog, Ui_ErrorRepairDialog):
    def __init__(self, parent=None):
        super(MyErrorRepairForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.selectFileBtn.clicked.connect(self.select_file)
        self.repairBtn.clicked.connect(self.repair)
        self.maxRecursionLineEdit.setValidator(QIntValidator(1, 65535, self))
        self.maxRecursionLineEdit.setText('32')
        self.repair_thread = None
        _thread.start_new_thread(self.update, ())

    def repair(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                t = repairThread(path, int(self.maxRecursionLineEdit.text()))
                self.repair_thread = t
                t.start()
                self.setDisabled(True)
                self.repairBtn.setText(QCoreApplication.translate('ErrorRepairDialog', 'is repairing...', None))

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self, 'select the game file', '', "Game Files (*.exe)")
        self.selectFileText.setText(file)

    def update(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self):
        try:
            if self.repair_thread is not None:
                if not self.repair_thread.is_alive():
                    self.repairBtn.setText(QCoreApplication.translate('ErrorRepairDialog', 'repair errors', None))
                    self.setEnabled(True)
                    self.repair_thread = None
                    log_print('error repair complete!')
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