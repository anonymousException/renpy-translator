import _thread
import os
import subprocess
import threading
import time
import traceback

from PySide6.QtCore import QCoreApplication, QThread, Signal, Qt
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel, QAction
from PySide6.QtWidgets import QDialog, QFileDialog, QMenu

from my_log import log_print
from html_util import open_directory_and_select_file

from call_game_python import get_py_path, get_python_path_from_game_path
from pack_game import Ui_PackGameDialog
import add_change_language_entrance_form
import my_log
from extraction_form import DirectorySelector


class packThread(threading.Thread):
    def __init__(self, path, package_name, pack_list, is_show_directory):
        threading.Thread.__init__(self)
        self.path = path
        self.package_name = package_name
        self.is_show_directory = is_show_directory
        self.pack_list = pack_list

    def run(self):
        try:
            log_print('start pack game files...')

            pack_game_files(self.path, self.package_name, self.pack_list, self.is_show_directory)
            log_print('pack game files complete!')
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


class MyPackGameForm(QDialog, Ui_PackGameDialog):
    def __init__(self, parent=None):
        super(MyPackGameForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('main.ico'))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.selectFileBtn.clicked.connect(self.select_file)
        self.packBtn.clicked.connect(self.pack)
        self.pack_thread = None
        self.selectDirsBtn.clicked.connect(self.on_select_dirs_clicked)
        self.selectFilesBtn.clicked.connect(self.on_select_files_clicked)
        self.selectFileText.textChanged.connect(self.on_select_file_text_changed)
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.setStyleSheet("""
            QListView::item {
                border-bottom: 1px solid black;
                padding: 5px;
            }
        """)
        self.listView.customContextMenuRequested.connect(self.open_menu)
        self.appendButton.clicked.connect(self.on_append_button_clicked)
        self.autoCopyTranslationCheckBox.clicked.connect(self.on_auto_copy_translation_clicked)
        self.autoCopyFontCheckBox.clicked.connect(self.on_auto_copy_font_clicked)
        _thread.start_new_thread(self.update, ())

    def on_auto_copy_font_clicked(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                game_dir = dir + '/game'
                font_file_list = get_font_file_list(game_dir)
                item_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row).data()
                    item_list.append(item)
                if self.autoCopyFontCheckBox.isChecked():
                    for i in font_file_list:
                        if i not in item_list:
                            basename = i[len(game_dir):].strip('/').strip('\\')
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(i)
                            item.setData(i)
                            self.model.appendRow(item)
                            item_list.append(item)
                else:
                    for i in item_list:
                        if i in font_file_list:
                            target_row = None
                            for row in range(self.model.rowCount()):
                                item = self.model.item(row).data()
                                if item == i:
                                    target_row = row
                                    break
                            if target_row is not None:
                                self.model.removeRow(target_row)

    def on_auto_copy_translation_clicked(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                game_dir = dir + '/game'
                tl_dir = game_dir + '/tl'
                script_file_list = get_script_file_list(game_dir)
                target_list = script_file_list
                item_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row).data()
                    item_list.append(item)
                if self.autoCopyTranslationCheckBox.isChecked():
                    if tl_dir not in item_list:
                        basename = tl_dir[len(game_dir):].strip('/').strip('\\')
                        item = QStandardItem(f'{basename}')
                        item.setToolTip(tl_dir)
                        item.setData(tl_dir)
                        self.model.appendRow(item)
                        item_list.append(item)
                    for i in target_list:
                        if i not in item_list:
                            basename = i[len(game_dir):].strip('/').strip('\\')
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(i)
                            item.setData(i)
                            self.model.appendRow(item)
                            item_list.append(item)
                else:
                    for i in item_list:
                        if i in target_list or i == tl_dir:
                            target_row = None
                            for row in range(self.model.rowCount()):
                                item = self.model.item(row).data()
                                if item == i:
                                    target_row = row
                                    break
                            if target_row is not None:
                                self.model.removeRow(target_row)



    def open_menu(self, position):
        indexes = self.listView.selectedIndexes()

        if len(indexes) > 0:
            menu = QMenu()
            delete_action = QAction(QCoreApplication.translate('PackGameDialog',
                                                               'Delete',
                                                               None), self)
            menu.addAction(delete_action)
            delete_action.triggered.connect(lambda: self.delete_item(indexes))
            menu.exec(self.listView.viewport().mapToGlobal(position))

    def delete_item(self, indexes):
        for index in indexes:
            self.model.removeRow(index.row())

    def on_append_button_clicked(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                game_dir = dir + '/game'
                game_dir = game_dir.replace('\\', '/')
                game_dir = game_dir.strip('/').strip('\\')
                item_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row).data()
                    item_list.append(item)
                select_files = self.selectFilesText.toPlainText().split('\n')
                select_dirs = self.selectDirsText.toPlainText().split('\n')
                for i in select_files:
                    i = i.replace('file:///', '')
                    i = i.replace('\\', '/')
                    i = i.strip('/').strip('\\')
                    if len(i) > 0 and os.path.isfile(i):
                        if i not in item_list:
                            basename = i[len(game_dir) + 1:]
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(i)
                            item.setData(i)
                            self.model.appendRow(item)
                            item_list.append(item)
                for i in select_dirs:
                    i = i.replace('file:///', '')
                    i = i.replace('\\', '/')
                    i = i.strip('/').strip('\\')
                    if len(i) > 0 and os.path.isdir(i):
                        if i not in item_list:
                            basename = i[len(game_dir) + 1:]
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(i)
                            item.setData(i)
                            self.model.appendRow(item)
                            item_list.append(item)
                self.on_auto_copy_translation_clicked()
                self.on_auto_copy_font_clicked()

    def on_select_file_text_changed(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        if os.path.isfile(path):
            if path.endswith('.exe'):
                dir = os.path.dirname(path)
                game_dir = dir + '/game'
                item_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row).data()
                    item_list.append(item)
                if self.autoCopyFontCheckBox.isChecked():
                    font_file_list = get_font_file_list(game_dir)
                    for i in font_file_list:
                        if i not in item_list:
                            basename = i[len(game_dir):].strip('/').strip('\\')
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(i)
                            item.setData(i)
                            self.model.appendRow(item)
                            item_list.append(item)
                if self.autoCopyTranslationCheckBox.isChecked():
                    script_file_list = get_script_file_list(game_dir)
                    for i in script_file_list:
                        if i not in item_list:
                            basename = i[len(game_dir):].strip('/').strip('\\')
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(i)
                            item.setData(i)
                            self.model.appendRow(item)
                            item_list.append(item)
                    tl_dir = game_dir + '/tl'
                    if os.path.isdir(tl_dir):
                        if tl_dir not in item_list:
                            basename = tl_dir[len(game_dir):].strip('/').strip('\\')
                            item = QStandardItem(f'{basename}')
                            item.setToolTip(tl_dir)
                            item.setData(tl_dir)
                            self.model.appendRow(item)
                            item_list.append(tl_dir)
        else:
            self.model.clear()

    def on_select_files_clicked(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        target_dir = ''
        if os.path.isfile(path):
            if path.endswith('.exe'):
                target_dir = os.path.dirname(path) + '/game'
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       QCoreApplication.translate('PackGameDialog',
                                                                                  'select the file(s) you want to pack',
                                                                                  None),
                                                       target_dir,
                                                       "All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText.setText(s.rstrip('\n'))

    def on_select_dirs_clicked(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        target_dir = None
        if os.path.isfile(path):
            if path.endswith('.exe'):
                target_dir = os.path.dirname(path) + '/game'
        directorySelector = DirectorySelector(target_dir)
        if directorySelector.exec() == 1:
            folders = directorySelector.selectedFiles()
            s = ''
            for folder in folders:
                if os.path.isdir(folder):
                    s = s + folder + '\n'
            self.selectDirsText.setText(s.rstrip('\n'))

    def closeEvent(self, event):
        self.parent.widget.show()
        self.parent.menubar.show()
        self.parent.versionLabel.show()
        self.parent.actionpack_game_files.triggered.connect(
            lambda: self.parent.show_pack_game_files_form())
        self.parent.show()
        self.hide()
        event.ignore()
        return

    def pack(self):
        path = self.selectFileText.toPlainText()
        path = path.replace('file:///', '')
        package_name = self.packageNameText.toPlainText().strip('\n').strip()
        if len(package_name) == 0:
            log_print('package name should not be empty')
            self.parent.show()
            self.parent.raise_()
            return
        if os.path.isfile(path):
            if path.endswith('.exe'):
                pack_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row).data()
                    pack_list.append(item)
                t = packThread(path, package_name, pack_list, True)
                self.pack_thread = t
                t.start()
                self.setDisabled(True)
                self.parent.show()
                self.parent.raise_()
                self.hide()
                self.packBtn.setText(QCoreApplication.translate('PackGameDialog', 'is packing...', None))

    def select_file(self):
        file, filetype = QFileDialog.getOpenFileName(self,
                                                     QCoreApplication.translate('PackGameDialog',
                                                                                'select the game file you want to pack it\'s files',
                                                                                None),
                                                     '',
                                                     "Game Files (*.exe)")
        self.selectFileText.setText(file)

    def update(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self):
        try:
            if self.pack_thread is not None:
                if not self.pack_thread.is_alive():
                    self.packBtn.setText(QCoreApplication.translate('PackGameDialog', 'pack game files', None))
                    self.show()
                    self.raise_()
                    self.setEnabled(True)
                    self.pack_thread = None

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


def is_font_file(file_name):
    font_suffix = ['.ttf', '.eot', '.otf', '.woff', '.svg', '.ttc']
    for i in font_suffix:
        if file_name.endswith(i):
            return True
    return False


def get_font_file_list(game_dir):
    font_file_list = []
    paths = os.walk(game_dir, topdown=False)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if not is_font_file(i):
                continue
            font_file_list.append(i)
    return font_file_list


def pack_from_list(python_path, pack_list, target_path):
    rpa_script_path = os.getcwd() + '/rpatool'
    game_dir = os.path.dirname(target_path)
    if len(pack_list) > 0:
        if not os.path.isfile(target_path):
            i = pack_list[0]
            basename = i[len(game_dir):].strip('/').strip('\\')
            command = '"' + python_path + '"' + f' -O "{rpa_script_path}" -c "{target_path}" "{basename}"="{i}"'
            log_print(command)
            p = subprocess.Popen(command, shell=True, stdout=my_log.f, stderr=my_log.f,
                                 creationflags=0x08000000, text=True, encoding='utf-8')
            p.wait()
            pack_list.pop(0)
        for i in pack_list:
            basename = i[len(game_dir):].strip('/').strip('\\')
            command = '"' + python_path + '"' + f' -O "{rpa_script_path}" -a "{target_path}" "{basename}"="{i}"'
            log_print(command)
            p = subprocess.Popen(command, shell=True, stdout=my_log.f, stderr=my_log.f,
                                 creationflags=0x08000000, text=True, encoding='utf-8')
            p.wait()


def get_script_file_list(game_dir):
    l = []
    script_path = game_dir + '/' + add_change_language_entrance_form.hook_script
    if os.path.isfile(script_path):
        l.append(script_path)

    if os.path.isfile(script_path + 'c'):
        l.append(script_path + 'c')
    return l


def pack_game_files(path, package_name, pack_list, is_show_directory):
    dir = os.path.dirname(path)
    game_dir = dir + '/game'
    python_path = get_python_path_from_game_path(path)
    if python_path is None:
        log_print(f'can not locate python.exe , please check {path}')
    target_path = dir + '/game/' + package_name + '.rpa'
    # tl_dir = game_dir + '/tl/'
    # font_file_list = get_font_file_list(game_dir)
    # pack_list.extend(font_file_list)
    # script_file_list = get_script_file_list(game_dir)
    # pack_list.extend(script_file_list)
    # pack_list.append(tl_dir)

    pack_from_list(python_path, pack_list, target_path)

    if is_show_directory:
        open_directory_and_select_file(target_path)
