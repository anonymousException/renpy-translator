import _thread
import os
import traceback

from PySide6.QtCore import QCoreApplication, QDir
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog, QFileDialog, QListView, QAbstractItemView, QTreeView

from my_log import log_print
from extraction import Ui_ExtractionDialog
from renpy_extract import extractThread, extract_threads


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


class MyExtractionForm(QDialog, Ui_ExtractionDialog):
    def __init__(self, parent=None):
        super(MyExtractionForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.extractBtn.clicked.connect(self.extract)
        self.selectFilesBtn_2.clicked.connect(self.select_file2)
        self.selectDirBtn_2.clicked.connect(self.select_directory2)

        self.selectDirsBtn.clicked.connect(self.select_directory4)
        self.filterCheckBox.setChecked(True)
        self.filterLengthLineEdit.setText('8')
        self.filterCheckBox.stateChanged.connect(self.filter_checkbox_changed)
        validator = QIntValidator()
        self.filterLengthLineEdit.setValidator(validator)

    def filter_checkbox_changed(self, state):
        if self.filterCheckBox.isChecked():
            self.filterLengthLineEdit.setEnabled(True)
        else:
            self.filterLengthLineEdit.setDisabled(True)

    def select_directory4(self):
        directorySelector = DirectorySelector()
        if directorySelector.exec() == 1:
            folders = directorySelector.selectedFiles()
            s = ''
            for folder in folders:
                if os.path.isdir(folder):
                    s = s + folder + '\n'
            self.selectDirsText.setText(s.rstrip('\n'))

    def select_file2(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       QCoreApplication.translate('MainWindow',
                                                                                  'select the file(s) you want to extract',
                                                                                  None),
                                                       '',
                                                       "Rpy Files (*.rpy);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText_2.setText(s.rstrip('\n'))

    def select_directory2(self):
        directory = QFileDialog.getExistingDirectory(self, QCoreApplication.translate('MainWindow',
                                                                                      'select the directory you want to extract',
                                                                                      None))
        self.selectDirText_2.setText(directory)

    def extract(self):
        # noinspection PyBroadException
        try:
            select_files = self.selectFilesText_2.toPlainText().split('\n')
            cnt = 0
            for i in select_files:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    tl_name = self.tlNameText.toPlainText()
                    if len(tl_name) == 0:
                        log_print('tl name is empty skip extract file(s)')
                        continue
                    t = extractThread(threadID=cnt, p=i, tl_name=tl_name, dirs=None, tl_dir=None,
                                      is_open_filter=self.filterCheckBox.isChecked(),
                                      filter_length=int(self.filterLengthLineEdit.text()),
                                      is_gen_empty=self.emptyCheckBox.isChecked(), is_skip_underline=self.underlineCheckBox.isChecked())
                    extract_threads.append(t)
                    cnt = cnt + 1
            select_dirs = self.selectDirsText.toPlainText().split('\n')
            _dirs = []
            for i in select_dirs:
                i = i.replace('file:///', '')
                if len(i) > 0:
                    _dirs.append(i)
            if len(_dirs) > 0:
                tl_name = self.tlNameText.toPlainText()
                if len(tl_name) == 0:
                    log_print('tl name is empty skip extract directory(s)')
                else:
                    t = extractThread(threadID=cnt, p=None, tl_name=tl_name, dirs=_dirs, tl_dir=None,
                                      is_open_filter=self.filterCheckBox.isChecked(),
                                      filter_length=int(self.filterLengthLineEdit.text()),
                                      is_gen_empty=self.emptyCheckBox.isChecked(), is_skip_underline=self.underlineCheckBox.isChecked())
                    extract_threads.append(t)
                    cnt = cnt + 1
            select_dir = self.selectDirText_2.toPlainText()
            if len(select_dir) > 0:
                select_dir = select_dir.replace('file:///', '')
                tl_name = self.tlNameText.toPlainText()
                if not os.path.exists(select_dir):
                    log_print(select_dir + ' directory does not exist!')
                else:
                    if select_dir[len(select_dir) - 1] != '/' and select_dir[len(select_dir) - 1] != '\\':
                        select_dir = select_dir + '/'
                    t = extractThread(threadID=cnt, p=None, tl_name=tl_name, dirs=None, tl_dir=select_dir,
                                      is_open_filter=self.filterCheckBox.isChecked(),
                                      filter_length=int(self.filterLengthLineEdit.text()),
                                      is_gen_empty=self.emptyCheckBox.isChecked(), is_skip_underline=self.underlineCheckBox.isChecked())
                    extract_threads.append(t)
                    cnt = cnt + 1
            if len(extract_threads) > 0:
                self.parent.extracting = True
                self.extractBtn.setText(QCoreApplication.translate('MainWindow', 'is extracting...', None))
                self.extractBtn.setDisabled(True)
                for t in extract_threads:
                    t.start()
                _thread.start_new_thread(self.extract_threads_over, ())
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            self.parent.extracting = False

    def extract_threads_over(self):
        while True:
            threads_len = len(extract_threads)
            if threads_len > 0:
                for t in extract_threads:
                    if t.is_alive():
                        t.join()
                    extract_threads.remove(t)
            else:
                break
        log_print('extract all complete!')
        self.parent.extracting = False
