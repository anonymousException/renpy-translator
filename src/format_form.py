import _thread
import os
import traceback

from PySide6.QtCore import QCoreApplication, QDir
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog, QFileDialog, QListView, QAbstractItemView, QTreeView

from my_log import log_print
from renpy_format import formatThread, format_threads
from format import Ui_FormatDialog


class DirectorySelector(QFileDialog):
    def __init__(self, base_dir=None):
        super(DirectorySelector, self).__init__()
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        if base_dir is None:
            self.setDirectory(QDir.rootPath())
        else:
            self.setDirectory(base_dir)
        listView = self.findChild(QListView, "listView")
        if listView:
            listView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        treeView = self.findChild(QTreeView, "treeView")
        if treeView:
            treeView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)


class MyFormationForm(QDialog, Ui_FormatDialog):
    def __init__(self, parent=None):
        super(MyFormationForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.formatBtn.clicked.connect(self.format)
        self.selectFilesBtn.clicked.connect(self.select_file)
        self.selectDirsBtn.clicked.connect(self.select_directory)

    def select_directory(self):
        directorySelector = DirectorySelector()
        if directorySelector.exec() == 1:
            folders = directorySelector.selectedFiles()
            s = ''
            for folder in folders:
                if os.path.isdir(folder):
                    s = s + folder + '\n'
            self.selectDirsText.setText(s.rstrip('\n'))

    def select_file(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       '',
                                                       '',
                                                       "Rpy Files (*.rpy);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText.setText(s.rstrip('\n'))



    def format(self):
        # noinspection PyBroadException
        try:
            select_files = self.selectFilesText.toPlainText().split('\n')
            for i in select_files:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    t = formatThread(p=i, dirs=None)
                    format_threads.append(t)
            select_dirs = self.selectDirsText.toPlainText().split('\n')
            _dirs = []
            for i in select_dirs:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    _dirs.append(i)
            if len(_dirs) > 0:
                t = formatThread(p=None, dirs=_dirs)
                format_threads.append(t)

            if len(format_threads) > 0:
                self.parent.formating = True
                self.formatBtn.setText(QCoreApplication.translate('FormatDialog', 'is formating...', None))
                self.formatBtn.setDisabled(True)
                for t in format_threads:
                    t.start()
                _thread.start_new_thread(self.format_threads_over, ())
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            self.parent.formating = False

    def format_threads_over(self):
        while True:
            threads_len = len(format_threads)
            if threads_len > 0:
                for t in format_threads:
                    if t.is_alive():
                        t.join()
                    format_threads.remove(t)
            else:
                break
        log_print('format all complete!')
        self.parent.formating = False
