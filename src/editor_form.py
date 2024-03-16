import _thread
import json
import multiprocessing

import os.path
import io
import threading
import time
import traceback

from PySide6 import QtCore
from PySide6.QtCore import Qt, QDir, QModelIndex, QSortFilterProxyModel, Signal, QThread
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QColor, QTextCursor, QKeySequence
from PySide6.QtWidgets import QDialog, QHeaderView, QTableView, QMenu, QListView, QFileDialog, QTreeView, \
    QFileSystemModel, QStyle, QMessageBox, QButtonGroup, QInputDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, \
    QCheckBox, QLineEdit
from editor import Ui_EditorDialog
from my_log import log_print, log_path
from renpy_translate import init_client, TranslateToList, engineDic, language_header
from custom_engine_form import targetDic, sourceDic
from engine_form import MyEngineForm
from string_tool import *

addedList = []
rpy_info_dic = dict()
translated_thread = None
translated_dic = None
is_need_save = False


class CustomSortProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(CustomSortProxyModel, self).__init__(parent)
        self.filter_pattern = '.rpy'

    def lessThan(self, left, right):
        if left.column() > 0 and right.column() > 0:
            leftValue = 0
            rightValue = 0
            if len(left.data()) > 0:
                leftValue = float(left.data().strip('%'))
            if len(right.data()) > 0:
                rightValue = float(right.data().strip('%'))
            return leftValue < rightValue
        else:
            return super().lessThan(left, right)

    def filterAcceptsRow(self, source_row, source_parent):
        index0 = self.sourceModel().index(source_row, 0, source_parent)
        file_name = self.sourceModel().fileName(index0)
        if self.sourceModel().isDir(index0) or file_name.endswith(self.filter_pattern):
            return True
        else:
            return False


class FileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_open_filter = True

    def columnCount(self, parent=QModelIndex()):
        return super().columnCount(parent) + 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and index.column() == 4:
            path = index.sibling(index.row(), 0).data()
            full_path = self.filePath(index)
            # info = self.fileInfo(self.index(index.row(), 0, index.parent()))
            # full_path = info.absoluteFilePath()
            if os.path.isfile(full_path):
                if full_path in rpy_info_dic.keys():
                    ret, unmatch_cnt, p = rpy_info_dic[full_path]
                else:
                    return ''
                    ret, unmatch_cnt, p = get_rpy_info(full_path)
                rpy_info_dic[full_path] = ret, unmatch_cnt, p
                return str(len(ret))
            else:
                return ''
        elif role == Qt.DisplayRole and index.column() == 5:
            path = index.sibling(index.row(), 0).data()
            full_path = self.filePath(index)
            # info = self.fileInfo(self.index(index.row(), 0, index.parent()))
            # full_path = info.absoluteFilePath()
            if os.path.isfile(full_path):
                if full_path in rpy_info_dic.keys():
                    ret, unmatch_cnt, p = rpy_info_dic[full_path]
                else:
                    return ''
                    ret, unmatch_cnt, p = get_rpy_info(full_path)
                rpy_info_dic[full_path] = ret, unmatch_cnt, p
                if len(ret) != 0:
                    percentage = unmatch_cnt / len(ret) * 100
                else:
                    percentage = 0
                return f'{percentage:.2f}%'
            else:
                return ''
        else:
            return super().data(index, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole and
                section == self.columnCount() - 2):
            return 'Units'
        if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole and
                section == self.columnCount() - 1):
            return 'Translated'

        return super().headerData(section, orientation, role)


class MyTreeView(QTreeView):

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setColumnWidth(0, self.width() * 0.5)

    def __init__(self, parent=None):
        super(MyTreeView, self).__init__(parent)
        self.setWindowTitle("Dir View")
        self.model = FileSystemModel()
        self.model.setRootPath('/')
        self.proxy_model = CustomSortProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.setRootIndex(self.proxy_model.mapFromSource(self.model.index('/')))
        for i in [1, 2, 3]:
            self.setColumnHidden(i, True)
        self.header().sectionClicked.connect(self.handle_header_clicked)
        self.setSortingEnabled(True)
        self.asc = True
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        # self.hide()

    def refresh_table_view(self, full_path):
        if os.path.isfile(full_path):
            self.tableView.model.clear()
            self.tableView.searched.clear()
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableView.model.setHorizontalHeaderLabels(['line', 'refer', 'Original', 'Current', 'Translated'])
            if full_path in rpy_info_dic.keys():
                ret, unmatch_cnt, p = rpy_info_dic[full_path]
            else:
                ret, unmatch_cnt, p = get_rpy_info(full_path)
                rpy_info_dic[full_path] = ret, unmatch_cnt, p
            for i in ret:
                row = [
                    QStandardItem(str(i['line'])),
                    QStandardItem(i['refer']),
                    QStandardItem(i['original']),
                    QStandardItem(i['current']),
                    QStandardItem(''),
                ]
                for item in row:
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setToolTip(item.text())
                row[0].setData(i, Qt.UserRole)
                row[0].setEditable(False)
                row[1].setEditable(False)
                row[2].setEditable(False)
                self.tableView.model.appendRow(row)
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.tableView.file = full_path
            self.tableView.index = self.currentIndex()

    def on_selection_changed(self, selected, deselected):
        selected_indexes = selected.indexes()
        if len(selected_indexes) > 0:
            index = self.currentIndex()
            source_index = self.proxy_model.mapToSource(index)
            file_info = QtCore.QFileInfo(self.model.filePath(source_index))
            full_path = file_info.absoluteFilePath()
            full_path = full_path.replace('\\', '/')
            self.refresh_table_view(full_path)

    def handle_header_clicked(self, index):
        if self.asc:
            self.sortByColumn(index, Qt.AscendingOrder)
            self.asc = False
        else:
            self.sortByColumn(index, Qt.DescendingOrder)
            self.asc = True


class MySelectTableView(QTableView):
    def __init__(self, parent=None):
        super(MySelectTableView, self).__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Path', 'Units', 'Translated'])
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(35)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSortingEnabled(True)
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def load_data(self, index):
        if index.isValid():
            select_one = index.data()
            if self.treeView.model.is_open_filter:
                self.treeView.proxy_model.filter_pattern = '.rpy'
            else:
                self.treeView.proxy_model.filter_pattern = ''
            if os.path.isdir(select_one):
                self.rpyCheckBox.setDisabled(True)
                rpy_info_dic.clear()
                self.tableView.model.clear()
                self.tableView.searched.clear()
                t = getRpyInfoThread(p=select_one, is_open_filter=self.treeView.model.is_open_filter)
                t.start()
                self.setDisabled(True)
                self.treeView.setDisabled(True)
                self.treeView.show()
            else:
                if (os.path.isfile(select_one)):
                    rpy_info_dic.clear()
                    self.tableView.model.clear()
                    self.tableView.searched.clear()
                    self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tableView.model.setHorizontalHeaderLabels(
                        ['line', 'refer', 'Original', 'Current', 'Translated'])

                    ret, unmatch_cnt, p = get_rpy_info(select_one)
                    rpy_info_dic[select_one] = ret, unmatch_cnt, p
                    for i in ret:
                        row = [
                            QStandardItem(str(i['line'])),
                            QStandardItem(i['refer']),
                            QStandardItem(i['original']),
                            QStandardItem(i['current']),
                            QStandardItem(''),
                        ]
                        for item in row:
                            item.setTextAlignment(Qt.AlignCenter)
                            item.setToolTip(item.text())
                        row[0].setData(i, Qt.UserRole)
                        row[0].setEditable(False)
                        row[1].setEditable(False)
                        row[2].setEditable(False)
                        self.tableView.model.appendRow(row)
                    self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
                    self.tableView.file = select_one
                    self.tableView.index = index
                self.treeView.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            self.load_data(index)
        super(MySelectTableView, self).mousePressEvent(event)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        selected_rows = [index.row() for index in self.selectionModel().selectedRows()]

        if selected_rows:
            action1 = contextMenu.addAction("Remove", self.removeAction)

        contextMenu.exec_(event.globalPos())

    def removeAction(self):
        selected_indexes = self.selectionModel().selectedRows()
        selected_rows = [index.row() for index in selected_indexes]
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            addedList.remove(self.model.item(row, 0).text().replace('file:///', ''))
            self.model.removeRow(row)
        self.selectionModel().clearSelection()

    def resizeEvent(self, event):
        width = self.width()
        self.setColumnWidth(0, width * 0.7)
        self.setColumnWidth(1, width * 0.15)
        self.setColumnWidth(2, width * 0.14)
        super(MySelectTableView, self).resizeEvent(event)

    def act1(self):
        print("act1")


class translateThread(threading.Thread):
    def __init__(self, threadID, client, transList, target_language, source_language):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client
        self.transList = transList
        self.target_language = target_language
        self.source_language = source_language

    def run(self):
        global translated_dic
        try:
            log_print('begin translate! please waiting...')
            translated_dic = TranslateToList(self.client, self.transList, self.target_language, self.source_language)

        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            translated_dic = None


class MyInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.label1 = QLabel()
        self.text_edit = QTextEdit()
        self.text_edit = QTextEdit()
        self.checkbox = QCheckBox()
        self.checkbox.setText('Case Sensitive')
        self.checkbox.setChecked(True)
        self.referCheckbox = QCheckBox()
        self.referCheckbox.setText('Search refer column')
        self.referCheckbox.setChecked(True)
        self.originalCheckbox = QCheckBox()
        self.originalCheckbox.setText('Search Original column')
        self.originalCheckbox.setChecked(True)
        self.currentCheckbox = QCheckBox()
        self.currentCheckbox.setText('Search Current column')
        self.currentCheckbox.setChecked(True)
        self.translatedCheckbox = QCheckBox()
        self.translatedCheckbox.setText('Search Translated column')
        self.translatedCheckbox.setChecked(True)
        layout.addWidget(self.label1)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.referCheckbox)
        layout.addWidget(self.originalCheckbox)
        layout.addWidget(self.currentCheckbox)
        layout.addWidget(self.translatedCheckbox)
        button = QPushButton('OK')
        button.clicked.connect(self.accept)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setMinimumWidth(1000)

    def getText(self):
        return self.text_edit.toPlainText()


class MyInputJumpLineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.label1 = QLabel()
        self.text_edit = QLineEdit()
        layout.addWidget(self.label1)
        layout.addWidget(self.text_edit)
        button = QPushButton('OK')
        button.clicked.connect(self.accept)
        layout.addWidget(button)
        self.setLayout(layout)

    def getText(self):
        return self.text_edit.text()


class MyTableView(QTableView):
    def __init__(self, parent=None):
        super(MyTableView, self).__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['line', 'refer', 'Original', 'Current', 'Translated'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.is_original = False
        self.model.dataChanged.connect(self.handle_data_changed)
        self.file = None
        self.row = None
        self.searched = set()

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Find):
            self.search()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_G:
            self.jump_line()
        else:
            super().keyPressEvent(event)

    def jump_line(self):
        dialog = MyInputJumpLineDialog(self)
        dialog.setWindowTitle('Input Dialog')
        dialog.label1.setText('Please Input the line number you want to jump')
        if dialog.exec():
            text = dialog.getText()
            for row in range(self.model.rowCount()):
                item = self.model.item(row, 0)
                if item and item.text() == text:
                    self.selectRow(row)

    def search(self):
        dialog = MyInputDialog(self)
        dialog.setWindowTitle('Input Dialog')
        dialog.label1.setText('Please Input the content you want to search')
        if dialog.exec():
            self.searched.clear()
            search_text = dialog.getText()
            if len(search_text) == 0:
                return
            match_count = 0
            for row in range(self.model.rowCount()):
                is_match = False
                for column in range(self.model.columnCount()):
                    if column == 0:
                        continue
                    if not dialog.referCheckbox.isChecked() and column == 1:
                        continue
                    if not dialog.originalCheckbox.isChecked() and column == 2:
                        continue
                    if not dialog.currentCheckbox.isChecked() and column == 3:
                        continue
                    if not dialog.translatedCheckbox.isChecked() and column == 4:
                        continue
                    if self.verticalHeader().isSectionHidden(row):
                        continue
                    item = self.model.item(row, column)
                    if item:
                        item_text = item.text()
                        if not dialog.checkbox.isChecked():
                            item_text = item_text.lower()
                            search_text = search_text.lower()
                        if search_text in item_text:
                            self.selectRow(row)
                            self.searched.add(row)
                            is_match = True
                            log_print(f'search match line:{row} column{column} content:{item.text()}')
                            match_count = match_count + 1
                if not is_match:
                    self.verticalHeader().setSectionHidden(row, True)
                else:
                    self.verticalHeader().setSectionHidden(row, False)
            if match_count == 0:
                log_print('search not found!')
            else:
                log_print(f'search match count:{match_count}')
            self.editorForm.searchedOnlyCheckBox.setChecked(True)
            if self.editorForm.logAfterSearchCheckBox.isChecked():
                self.editorForm.parent.showNormal()
                self.editorForm.parent.raise_()

    def handle_data_changed(self, top_left, bottom_right):
        top_row = top_left.row()
        bottom_row = bottom_right.row()
        left_column = top_left.column()
        right_column = bottom_right.column()

        for row in range(top_row, bottom_row + 1):
            for column in range(left_column, right_column + 1):
                index = self.model.index(row, 0)
                now_data = self.model.index(row, column).data()
                item = QStandardItem(index.model().itemFromIndex(index))
                new_data = item.data(Qt.UserRole)
                tmp_data = dict()
                tmp_data['original'] = new_data['original']
                tmp_data['current'] = new_data['current']
                if column == 0:
                    tmp_data['line'] = int(now_data)
                elif column == 1:
                    tmp_data['refer'] = now_data
                elif column == 2:
                    tmp_data['original'] = now_data
                elif column == 3:
                    tmp_data['current'] = now_data
                elif column == 4:
                    tmp_data['translated'] = now_data
                new_data['is_match'] = tmp_data['original'] == tmp_data['current']
                self.model.dataChanged.disconnect()
                item.setToolTip(now_data)
                column_count = self.model.columnCount()
                item.setData(new_data, Qt.UserRole)
                self.model.setItem(row, 0, item)
                self.model.dataChanged.connect(self.handle_data_changed)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        selected_rows = [index.row() for index in self.selectionModel().selectedRows()]

        if selected_rows:
            action1 = contextMenu.addAction("Translate Translation Source to Translated", self.translate)
            action2 = contextMenu.addAction("Copy Original to Current", self.copy_ori_to_cur)
            action3 = contextMenu.addAction("Copy Translated to Current", self.copy_translated_to_cur)
            action4 = contextMenu.addAction("Rollback Current to First Load", self.rollback_cur)

        contextMenu.exec_(event.globalPos())

    def rollback_cur(self):
        selected_indexes = self.selectionModel().selectedRows()
        selected_rows = [index.row() for index in selected_indexes]
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            current = self.model.item(row, 0).data(Qt.UserRole)['current']
            self.model.item(row, 3).setText(current)

    def translate(self):
        selected_indexes = self.selectionModel().selectedRows()
        self.selected_rows = [index.row() for index in selected_indexes]
        self.selected_rows.sort(reverse=True)
        transList = []
        for row in self.selected_rows:
            if self.is_original:
                target = self.model.item(row, 2).text()
            else:
                target = self.model.item(row, 3).text()
            d = EncodeBrackets(target)
            if (isAllPunctuations(d['encoded'].strip('"')) == False):
                transList.append(d['encoded'].strip('"'))
        if len(transList) == 0:
            return
        client = init_client()
        if client is None:
            return
        target_language = targetDic[self.editorForm.targetComboBox.currentText()]
        source_language = sourceDic[self.editorForm.sourceComboBox.currentText()]
        self.editorForm.parent.showNormal()
        self.editorForm.parent.raise_()
        self.editorForm.hide()
        self.editorForm.setDisabled(True)
        # trans_dic = TranslateToList(client, transList, target_language, source_language)
        global translated_thread, translated_dic
        translated_thread = translateThread(0, client, transList, target_language, source_language)
        translated_thread.start()

    def copy_translated_to_cur(self):
        selected_indexes = self.selectionModel().selectedRows()
        selected_rows = [index.row() for index in selected_indexes]
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            ori = self.model.item(row, 4).text()
            self.model.item(row, 3).setText(ori)

    def copy_ori_to_cur(self):
        selected_indexes = self.selectionModel().selectedRows()
        selected_rows = [index.row() for index in selected_indexes]
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            ori = self.model.item(row, 2).text()
            self.model.item(row, 3).setText(ori)


class MyEditorForm(QDialog, Ui_EditorDialog):
    def __init__(self, parent=None):
        super(MyEditorForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('main.ico'))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        addedList.clear()
        self.selectFilesBtn.clicked.connect(self.select_file)
        self.selectDirBtn.clicked.connect(self.select_directory)
        self.addListButton.clicked.connect(self.add_to_list)
        self.tableView = MyTableView()
        self.tableView.editorForm = self
        self.tableVerticalLayout.addWidget(self.tableView)
        self.selectTableView = MySelectTableView()
        self.fileVerticalLayout.addWidget(self.selectTableView)
        # item = QStandardItem('F:\\Games\\RenPy\\DemoGame\\game\\tl\\japanese\\script.rpy')
        # self.listView.model.appendRow(item)
        self.treeView = MyTreeView()
        self.fileVerticalLayout.addWidget(self.treeView)
        self.treeView.setMaximumWidth(550)
        self.selectTableView.setMaximumWidth(550)
        self.selectTableView.tableView = self.tableView
        self.selectTableView.treeView = self.treeView
        self.treeView.tableView = self.tableView
        self.rpyCheckBox.setChecked(True)
        self.selectTableView.rpyCheckBox = self.rpyCheckBox
        self.rpyCheckBox.stateChanged.connect(self.on_rpy_checkbox_state_changed)
        self.treeView.hide()
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.originalRadioButton, 1)
        self.buttonGroup.addButton(self.currentRadioButton, 2)
        self.buttonGroup.buttonClicked.connect(self.button_group_clicked)
        self.init_combobox()
        self.untranslatedCheckBox.stateChanged.connect(self.on_checkbox_state_changed)
        self.saveFileButton.clicked.connect(self.save_file_button_clicked)
        self.changeTranslationEngineButton.clicked.connect(self.show_engine_settings)
        self.showLogButton.clicked.connect(self.on_show_log_button_checked)
        self.searchedOnlyCheckBox.stateChanged.connect(self.on_checkbox_state_changed)
        _thread.start_new_thread(self.update_log, ())

    def on_show_log_button_checked(self):
        self.parent.showNormal()
        self.parent.raise_()

    def closeEvent(self, event):
        self.parent.widget.show()
        self.parent.widget_2.show()
        self.parent.widget_3.show()
        self.parent.menubar.show()
        self.parent.actionedit.triggered.connect(lambda: self.parent.show_edit_form())
        self.parent.showNormal()

    def show_engine_settings(self):
        engine_form = MyEngineForm(parent=self)
        ori = None
        now = None
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                ori = json.load(json_file)
        engine_form.exec()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                now = json.load(json_file)
        if (now is not None and ori is not None and now['engine'] != ori['engine']) \
                or (now is None and ori is None) \
                or (now is not None and ori is None):
            self.init_combobox()

    def save_file_button_clicked(self):
        if self.tableView.file is None:
            return
        log_print('start saving file! please waiting...')
        self.hide()
        self.setDisabled(True)
        self.parent.showNormal()
        self.parent.raise_()
        global is_need_save
        is_need_save = True

    def on_checkbox_state_changed(self):
        model = self.tableView.model
        rows = model.rowCount()
        columns = model.columnCount()
        for row in range(rows):
            for column in range(columns):
                index = model.index(row, 0)
                item = index.model().itemFromIndex(index)
                data = item.data(Qt.UserRole)
                if not data['is_match'] and self.untranslatedCheckBox.isChecked():
                    self.tableView.verticalHeader().setSectionHidden(row, True)
                else:
                    self.tableView.verticalHeader().setSectionHidden(row, False)

                if self.tableView.verticalHeader().isSectionHidden(row):
                    continue

                if len(self.tableView.searched) > 0 and self.searchedOnlyCheckBox.isChecked():
                    if row not in self.tableView.searched:
                        self.tableView.verticalHeader().setSectionHidden(row, True)
                    else:
                        self.tableView.verticalHeader().setSectionHidden(row, False)
                #log_print(f"Row: {row}, Column: {column}, Data: {data}")

    @staticmethod
    def get_combobox_content(p, d):
        f = io.open(p, 'r', encoding='utf-8')
        _read = f.read()
        f.close()
        _read_line = _read.split('\n')
        ret_l = []
        for i in _read_line:
            contents = i.split(':')
            d[contents[0].strip()] = contents[1].strip()
            ret_l.append(contents[0].strip())
        ret_l = list(set(ret_l))
        ret_l.sort()
        return ret_l

    def init_combobox(self):
        self.targetComboBox.clear()
        self.sourceComboBox.clear()
        target = 'google.target.rst'
        source = 'google.source.rst'
        customEngineDic = dict()
        if os.path.isfile('custom.txt'):
            f = io.open('custom.txt', 'r', encoding='utf-8')
            customEngineDic = json.load(f)
            f.close()
        if os.path.isfile('engine.txt'):
            with open('engine.txt', 'r') as json_file:
                loaded_data = json.load(json_file)
                if loaded_data['engine'] in engineDic:
                    target = engineDic[loaded_data['engine']]['target']
                    source = engineDic[loaded_data['engine']]['source']
                elif loaded_data['engine'] in customEngineDic:
                    target = customEngineDic[loaded_data['engine']]['target']
                    source = customEngineDic[loaded_data['engine']]['source']
                else:
                    log_print(loaded_data['engine'] + 'not in dic')
            if target is None or source is None:
                log_print('target or source not found!')
                return
            if len(target) == 0 or len(source) == 0:
                log_print('target or source is empty!')
                return
        target = language_header + target
        source = language_header + source
        target_l = self.get_combobox_content(target, targetDic)
        for i in target_l:
            self.targetComboBox.addItem(i)
        source_l = self.get_combobox_content(source, sourceDic)
        for i in source_l:
            self.sourceComboBox.addItem(i)
        try:
            self.sourceComboBox.setCurrentIndex(source_l.index('Auto Detect'))
        except Exception:
            pass

    def button_group_clicked(self, item):
        if item.group().checkedId() == 1:
            self.tableView.is_original = True
        else:
            self.tableView.is_original = False

    def on_rpy_checkbox_state_changed(self):
        if self.rpyCheckBox.isChecked():
            self.treeView.model.is_open_filter = True
        else:
            self.treeView.model.is_open_filter = False
        indexes = self.selectTableView.selectionModel().selectedIndexes()
        if indexes is not None and len(indexes) > 0:
            self.selectTableView.load_data(indexes[0])

    def add_to_list(self):
        select_files = self.selectFilesText.toPlainText().split('\n')
        cnt = 0
        for i in select_files:
            i = i.replace('file:///', '')
            if len(i) > 0 and os.path.isfile(i):
                if i not in addedList:
                    ret, unmatch_cnt, p = get_rpy_info(i)
                    if len(ret) != 0:
                        percentage = unmatch_cnt / len(ret) * 100
                    else:
                        percentage = 0
                    row = [
                        QStandardItem(i),
                        QStandardItem(str(len(ret))),
                        QStandardItem(f'{percentage:.2f}%'),
                    ]
                    for item in row:
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setEditable(False)
                        item.setToolTip(item.text())
                    row[0].setTextAlignment(Qt.AlignLeft)
                    self.selectTableView.model.appendRow(row)
                    addedList.append(i)
        self.selectTableView.model.sort(0, Qt.AscendingOrder)

        select_dir = self.selectDirText.toPlainText()
        select_dir = select_dir.replace('file:///', '')
        if len(select_dir) > 0 and os.path.isdir(select_dir):
            if select_dir not in addedList:
                row = [
                    QStandardItem(select_dir),
                    QStandardItem('/'),
                    QStandardItem('/'),
                ]
                for item in row:
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setEditable(False)
                    item.setToolTip(item.text())
                row[0].setTextAlignment(Qt.AlignLeft)
                self.selectTableView.model.appendRow(row)
                addedList.append(select_dir)
                self.selectTableView.model.sort(0, Qt.AscendingOrder)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'select the directory you want to edit')
        self.selectDirText.setText(directory)

    def select_file(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       "select the file(s) you want to edit",
                                                       '',
                                                       "Rpy Files (*.rpy);;All Files (*)")
        s = ''
        for file in files:
            s = s + file + '\n'
        self.selectFilesText.setText(s.rstrip('\n'))

    def update_log(self):
        thread = self.UpdateThread()
        thread.update_date.connect(self.update_progress)
        while True:
            thread.start()
            time.sleep(0.5)

    def update_progress(self, data):
        try:
            if os.path.isfile('rpy_info_got'):
                f = io.open('rpy_info_got', 'r', encoding='utf-8')
                select_one = f.read()
                f.close()
                self.treeView.model.setRootPath(select_one)
                self.treeView.setRootIndex(
                    self.treeView.proxy_model.mapFromSource(self.treeView.model.index(select_one)))
                self.treeView.proxy_model.invalidateFilter()
                self.treeView.model.setRootPath(select_one)
                self.treeView.setRootIndex(
                    self.treeView.proxy_model.mapFromSource(self.treeView.model.index(select_one)))
                self.selectTableView.setEnabled(True)
                self.treeView.setEnabled(True)
                self.rpyCheckBox.setEnabled(True)
                os.remove('rpy_info_got')

            global is_need_save
            if is_need_save:
                is_need_save = False
                f = io.open(self.tableView.file, 'r', encoding='utf-8')
                _read_lines = f.readlines()
                f.close()
                for row in range(self.tableView.model.rowCount()):
                    data = self.tableView.model.item(row, 0).data(Qt.UserRole)
                    line = int(data['line'])
                    ori_current = data['current']
                    current = self.tableView.model.item(row, 3).text()
                    if ori_current != current:
                        _read_lines[line] = _read_lines[line].replace(ori_current, current)
                f = io.open(self.tableView.file, 'w', encoding='utf-8')
                f.writelines(_read_lines)
                f.close()
                rpy_info_dic.clear()
                index = QModelIndex(self.tableView.index)
                item = self.selectTableView.model.item(index.row(), index.column())
                self.treeView.refresh_table_view(self.tableView.file)
                ret, unmatch_cnt, p = rpy_info_dic[self.tableView.file]
                if len(ret) != 0:
                    percentage = unmatch_cnt / len(ret) * 100
                else:
                    percentage = 0

                try:
                    if item is not None and item.index() == index:
                        self.selectTableView.model.item(index.row(), 2).setText(f'{percentage:.2f}%')
                        self.tableView.index = self.selectTableView.model.item(index.row(), 2).index()
                    else:
                        self.treeView.model.data(index)
                except Exception as e:
                    msg = traceback.format_exc()
                    log_print(msg)
                log_print('end saving file!')
                self.show()
                self.raise_()
                self.setEnabled(True)

            global translated_thread, translated_dic
            if translated_thread is None or translated_dic is None:
                return
            translated_thread.join()
            trans_dic = translated_dic
            for row in self.tableView.selected_rows:
                if self.tableView.is_original:
                    target = self.tableView.model.item(row, 2).text()
                else:
                    target = self.tableView.model.item(row, 3).text()
                d = EncodeBrackets(target)
                line_index = int(self.tableView.model.item(row, 0).text())
                if (isAllPunctuations(d['encoded'].strip('"')) == False):
                    try:
                        translated = trans_dic[d['encoded'].strip('"')]
                        translated = translated.replace('\u200b', '')
                        translated = translated.replace('\u200b1', '')
                        translated = translated.replace('"', '\\"')
                        translated = translated.replace('【', '[')
                        translated = translated.replace('】', ']')
                        translated = translated.rstrip('\\')
                        dd = DecodeBrackets(
                            translated, d['en_1'], d['en_2'], d['en_3'])
                        if d['en_1_cnt'] != dd['de_6_cnt'] or d['en_2_cnt'] != dd['de_5_cnt'] or d['en_3_cnt'] != \
                                dd[
                                    'de_4_cnt']:
                            raise Exception('decoded error')
                        dd = dd['decoded']
                        dd = dd.replace('&gt;', '>')
                        dd = dd.replace('&#39;', "'")
                        dd = dd.replace('&quot;', '\\"')
                        dd = dd.replace('\n', '\\n')
                        self.tableView.model.item(row, 4).setText(dd)
                        self.tableView.model.item(row, 4).setToolTip(dd)
                    except:
                        log_print(
                            'Error in line:' + str(line_index) + ' ' + '\n' + target + '\n' + d['encoded'].strip(
                                '"') + ' Error')
                        self.tableView.model.item(row, 4).setText(target)
                        self.tableView.model.item(row, 4).setToolTip(target)
                else:
                    self.tableView.model.item(row, 4).setText(target)
                    self.tableView.model.item(row, 4).setToolTip(target)
            # self.parent.hide()

            log_print('translated over')
            translated_dic = None
            translated_thread = None
            self.setEnabled(True)
            self.show()
            self.raise_()
        except Exception:
            msg = traceback.print_exc()
            log_print(msg)

    class UpdateThread(QThread):
        update_date = Signal(str)

        def __init__(self):
            super().__init__()

        def __del__(self):
            self.wait()

        def run(self):
            f = io.open(log_path, 'r', encoding='utf-8')
            self.update_date.emit(f.read())
            f.close()


class getRpyInfoThread(threading.Thread):
    def __init__(self, p, is_open_filter):
        threading.Thread.__init__(self)
        self.p = p
        self.is_open_filter = is_open_filter

    def run(self):
        try:
            get_rpy_info_from_dir(self.p, self.is_open_filter)
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('geting_rpy_info'):
                os.remove('geting_rpy_info')


def get_rpy_info_from_dir(select_one, is_open_filter):
    pool = multiprocessing.Pool(8)
    paths = os.walk(select_one, topdown=False)
    select_one = select_one.replace('\\', '/')
    jobs = []
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            if is_open_filter and not file_name.endswith("rpy"):
                continue
            i = os.path.join(path, file_name)
            jobs.append(i)

    res = pool.map(get_rpy_info, jobs)
    pool.close()
    pool.join()
    for ret, unmatch_cnt, p in res:
        p = p.replace('\\', '/')
        rpy_info_dic[p] = ret, unmatch_cnt, p

    f = io.open('rpy_info_got', 'w', encoding='utf-8')
    f.write(select_one)
    f.close()


def get_rpy_info(p):
    infoList = []
    log_print(f'start get rpy info : {p}')
    try:
        f = io.open(p, 'r', encoding='utf-8')
    except:
        log_print(p + ' file not found')
        return infoList, 0, p
    try:
        size = os.path.getsize(p)
        _read = f.read()
        f.close()
    except:
        f.close()
        return infoList, 0, p
    _read_line = _read.split('\n')
    isLastFiltered = False
    isNeedSkip = False
    unmatch_cnt = 0
    for line_index, line_content in enumerate(_read_line):
        if (line_content.startswith('translate ')):
            isNeedSkip = False
            split_s = line_content.split(' ')
            if (len(split_s) > 2):
                target = split_s[2].strip('\n')
                if (target == 'python:' or target == 'style'):
                    isNeedSkip = True
            continue
        if (isNeedSkip):
            continue
        isNeedSkip = False
        if (line_content.strip().startswith('#') or line_content.strip().startswith('old ')):
            isLastFiltered = True
            continue
        if (isLastFiltered):
            isLastFiltered = False
            # if (_read_line[line_index - 1].strip()[4:] != _read_line[line_index].strip()[4:] and _read_line[
            #                                                                                          line_index - 1].strip()[
            #                                                                                      2:] != _read_line[
            #     line_index].strip()):
            #     continue
        else:
            isLastFiltered = False
        if line_index > 0 and not _read_line[line_index - 1].strip().startswith('#') and not _read_line[
            line_index - 1].strip().startswith('old '):
            continue
        d = EncodeBracketContent(line_content, '"', '"')
        if ('oriList' in d.keys() and len(d['oriList']) > 0):
            # print(d['oriList'])
            for i, e in enumerate(d['oriList']):
                if (isAllPunctuations(d['encoded'].strip('"')) == False):
                    if line_content.strip().startswith('new '):
                        d_o = EncodeBracketContent(_read_line[line_index - 1].strip()[4:], '"', '"')
                    else:
                        d_o = EncodeBracketContent(_read_line[line_index - 1].strip(), '"', '"')
                    original = ''
                    if ('oriList' in d_o.keys() and len(d_o['oriList']) > 0):
                        original = d_o['oriList'][i].strip('"')
                    is_match = True
                    if original != e.strip('"'):
                        unmatch_cnt = unmatch_cnt + 1
                        is_match = False
                    dic = dict()
                    dic['original'] = original
                    dic['current'] = e.strip('"')
                    dic['line'] = line_index
                    start = line_index - 2
                    if line_content.strip().startswith('new '):
                        start = line_index
                    j = 0
                    end = start - 5
                    if end < 0:
                        end = -1
                    for j in range(start, end, -1):
                        if _read_line[j].strip().startswith('#'):
                            break
                    dic['refer'] = ''
                    if j != 0:
                        dic['refer'] = _read_line[j].strip('#')
                    dic['is_match'] = is_match
                    infoList.append(dic)
    # sorted(infoList, key=lambda x: x['line'])
    log_print(f'end get rpy info : {p}')
    return infoList, unmatch_cnt, p
