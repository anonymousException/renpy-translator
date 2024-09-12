# -*- coding: utf-8
import io
import random
import sys
import os
import threading
import time
import re
import traceback
import pathlib

from my_log import log_print
from call_game_python import is_python2_from_game_dir
from string_tool import remove_upprintable_chars, EncodeBracketContent, EncodeBrackets, replace_all_blank, \
    replace_unescaped_quotes

extract_threads = []

lock = threading.Lock()

num = 0
get_extracted_threads = []
get_extracted_lock = threading.Lock()
get_extracted_set_list = []


class ExtractTlThread(threading.Thread):
    def __init__(self, p, is_py2, is_remove_repeat_only = False):
        threading.Thread.__init__(self)
        self.p = p
        self.is_py2 = is_py2
        self.is_remove_repeat_only = is_remove_repeat_only

    def run(self):
        if not self.is_remove_repeat_only:
            extracted = ExtractFromFile(self.p, False, 9999, False, self.is_py2)
        else:
            remove_repeat_for_file(self.p)
            f = io.open(self.p, 'r', encoding='utf-8')
            _lines = f.readlines()
            f.close()
            f = io.open(self.p, 'w', encoding='utf-8')
            _lines = get_remove_consecutive_empty_lines(_lines)
            f.writelines(_lines)
            f.close()
            extracted = None
        get_extracted_lock.acquire()
        get_extracted_set_list.append((self.p, extracted))
        get_extracted_lock.release()


def remove_repeat_extracted_from_tl(tl_dir, is_py2):
    p = tl_dir
    if p[len(p) - 1] != '/' and p[len(p) - 1] != '\\':
        p = p + '/'
    e = set()
    paths = os.walk(p, topdown=False)
    global get_extracted_threads
    global get_extracted_set_list
    global get_extracted_lock
    cnt = 0
    get_extracted_set_list.clear()
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if file_name.endswith("rpy") == False:
                continue
            t = ExtractTlThread(i, is_py2)
            get_extracted_threads.append(t)
            cnt = cnt + 1
            t.start()
    while True:
        threads_len = len(get_extracted_threads)
        if threads_len > 0:
            for t in get_extracted_threads:
                if t.is_alive():
                    t.join()
                get_extracted_threads.remove(t)
        else:
            break
    i = 0
    while i < len(get_extracted_set_list):
        for k in range(i + 1, len(get_extracted_set_list)):
            p1, set1 = get_extracted_set_list[i]
            p2, set2 = get_extracted_set_list[k]
            both = set1 & set2
            if len(both) > 0:
                is_modified1 = False
                is_modified2 = False
                dic1 = dict()
                dic2 = dict()
                f = io.open(p1, 'r', encoding='utf-8')
                lines1 = f.readlines()
                f.close()
                f = io.open(p2, 'r', encoding='utf-8')
                lines2 = f.readlines()
                f.close()
                for j in both:
                    if not j.startswith('_p("""') and not j.endswith('""")'):
                        j = '"' + j + '"'
                    _cmp = '    old ' + j + '\n'
                    if lines1.count(_cmp) > 0 and lines2.count(_cmp) > 0:
                        _idx1 = lines1.index(_cmp)
                        _idx2 = lines2.index(_cmp)
                        _len1 = len(lines1)
                        _len2 = len(lines2)
                        is_both_old_new_format = False
                        if _idx1 + 1 < len(lines1) and lines1[_idx1 + 1].startswith('    new ') and _idx2 + 1 < len(
                                lines2) and lines2[_idx2 + 1].startswith('    new '):
                            is_both_old_new_format = True
                        if not is_both_old_new_format:
                            continue
                        if _len1 < _len2:
                            # log_print(
                            #     'Repeated Text Found in ' + p1 + ' ' + str(_idx1) + ' : \n' + lines1[_idx1].rstrip(
                            #         "\n") + '\n' +  lines1[_idx1 + 1].rstrip(
                            #         "\n"))
                            lines1[_idx1] = ''
                            lines1[_idx1 + 1] = ''
                            is_modified1 = True
                        else:
                            # log_print(
                            #     'Repeated Text Found in ' + p2 + ' ' + str(_idx2) + ' : \n' + lines2[_idx2].rstrip(
                            #         "\n") + '\n' + lines2[_idx2 + 1].rstrip(
                            #         "\n"))
                            lines2[_idx2] = ''
                            lines2[_idx2 + 1] = ''
                            is_modified2 = True
                if is_modified1:
                    f = io.open(p1, 'w', encoding='utf-8')
                    lines1 = get_remove_consecutive_empty_lines(lines1)
                    f.writelines(lines1)
                    f.close()
                    remove_repeat_for_file(p1)
                if is_modified2:
                    f = io.open(p2, 'w', encoding='utf-8')
                    lines2 = get_remove_consecutive_empty_lines(lines2)
                    f.writelines(lines2)
                    f.close()
                    remove_repeat_for_file(p2)
        i = i + 1

def get_remove_consecutive_empty_lines(lines):
    last_line_empty = False
    new_lines = []
    for line in lines:
        if line.strip() == '':
            if not last_line_empty:
                new_lines.append(line)
            last_line_empty = True
        else:
            new_lines.append(line)
            last_line_empty = False
    return new_lines


def remove_repeat_for_file(p):
    f = io.open(p, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    exist_set = set()
    is_removed = False
    is_empty_translate = True
    start_translate_block_line = -1
    for index, line in enumerate(lines):
        line = line.rstrip('\n')
        if (line.startswith('translate ') and line.endswith('strings:')) or index == len(lines) - 1:
            if start_translate_block_line != -1:
                if is_empty_translate:
                    is_removed = True
                    if index == len(lines) - 1:
                        index = index + 1
                    for idx in range(start_translate_block_line, index - 1):
                        lines[idx] = ''
                is_empty_translate = True
            start_translate_block_line = index
            continue
        if len(line) <= 4:
            continue
        if not line.startswith('    old "old:') and not line.startswith(
                '    new "new:') and not line.lstrip().startswith('#'):
            is_empty_translate = False
        if line not in exist_set:
            exist_set.add(line)
        else:
            if line.startswith('    old '):
                if (index + 1) <= len(lines):
                    new_line = lines[index + 1]
                    if new_line.startswith('    new '):
                        if line.startswith('    old ') and index > 0 and lines[index - 1].lstrip().startswith('#'):
                            lines[index - 1] = ''
                        # log_print('Remove Repeat in ' + p + ' ' + str(index) + ' : \n' + lines[index].rstrip(
                        #     "\n") + '\n' + new_line.rstrip("\n"))
                        lines[index] = ''
                        lines[index + 1] = ''
                        is_removed = True
    if is_removed:
        f = io.open(p, 'w', encoding='utf-8')
        lines = get_remove_consecutive_empty_lines(lines)
        f.writelines(lines)
        f.close()


class extractThread(threading.Thread):
    def __init__(self, threadID, p, tl_name, dirs, tl_dir, is_open_filter, filter_length, is_gen_empty,
                 is_skip_underline):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.p = p
        self.tl_name = tl_name
        self.dirs = dirs
        self.tl_dir = tl_dir
        self.is_open_filter = is_open_filter
        self.filter_length = filter_length
        self.is_gen_empty = is_gen_empty
        self.is_skip_underline = is_skip_underline

    def run(self):
        try:
            if self.tl_dir is not None and os.path.exists(self.tl_dir):
                self.tl_dir = self.tl_dir.rstrip('/')
                self.tl_dir = self.tl_dir.rstrip('\\')
                if self.tl_name is not None and len(self.tl_name) > 0:
                    ori_tl = os.path.basename(self.tl_dir)
                    self.tl_dir = self.tl_dir[:-len(ori_tl)] + self.tl_name
                log_print(self.tl_dir + ' begin extract!')
                ExtractAllFilesInDir(self.tl_dir, self.is_open_filter, self.filter_length, self.is_gen_empty,
                                     self.is_skip_underline)
            else:
                if self.p is not None:
                    self.p = self.p.replace('\\', '/')
                    log_print(self.p + ' begin extract!')
                    ExtractWriteFile(self.p, self.tl_name, self.is_open_filter, self.filter_length, self.is_gen_empty,
                                     set(), self.is_skip_underline)
                    remove_repeat_for_file(self.p)
                if self.dirs is not None:
                    global_e = set()
                    for _dir in self.dirs:
                        _dir = _dir.replace('\\', '/')
                        _dir = _dir.rstrip('/')
                        log_print(_dir + ' begin extract!')
                        paths = os.walk(_dir, topdown=False)
                        for path, dir_lst, file_lst in paths:
                            for file_name in file_lst:
                                i = os.path.join(path, file_name)
                                if not file_name.endswith("rpy"):
                                    continue
                                ret_e = ExtractWriteFile(i, self.tl_name, self.is_open_filter, self.filter_length,
                                                         self.is_gen_empty, global_e, self.is_skip_underline)
                                remove_repeat_for_file(i)
                                global_e = global_e | ret_e

        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


def is_path_or_dir_string(_string):
    if ' ' not in _string and ':' not in _string and '[' not in _string and '{' not in _string:
        if '\\' in _string or '/' in _string:
            return True
    return False


def ExtractFromFile(p, is_open_filter, filter_length, is_skip_underline, is_py2):
    remove_repeat_for_file(p)
    e = set()
    f = io.open(p, 'r+', encoding='utf-8')
    _read = f.read()
    f.close()
    # print(_read)
    _read_line = _read.split('\n')
    is_in_condition_switch = False
    is_in__p = False
    p_content = ''
    for index, line_content in enumerate(_read_line):
        if 'ConditionSwitch(' in line_content:
            if not line_content.strip().endswith(')'):
                is_in_condition_switch = True
            continue
        if _read_line[-1] == ')':
            is_in_condition_switch = False
            continue
        if is_in_condition_switch:
            continue

        cmp_line_content = remove_upprintable_chars(line_content.strip())
        if cmp_line_content.startswith('#') or len(line_content.strip()) == 0:
            continue

        if '_p("""' in line_content:
            is_in__p = True
            position = line_content.find('_p("""')
            p_content = line_content[position:] + '\n'
            continue

        if is_in__p:
            sep = '\n'
            if is_py2:
                sep = '\\n'
            p_content = p_content + line_content + sep
            if line_content.endswith('""")'):
                p_content = p_content.rstrip(sep)
                if is_py2:
                    p_content = p_content.strip()[6:-4]
                    p_content = p_content.rstrip('\n').replace('\n', '\\n')
                # log_print(p_content)
                if filter_length != 9999:
                    log_print(f'Found _p() in {p}:{index + 1}')
                e.add(p_content)
                is_in__p = False
                p_content = ''
            continue

        if is_open_filter:
            if cmp_line_content.startswith('label '):
                continue
            if line_content.strip().startswith('default '):
                continue
        # log_print(line_content)
        is_add = False
        d = EncodeBracketContent(line_content, '"', '"')
        if 'oriList' in d.keys() and len(d['oriList']) > 0:
            for i in d['oriList']:
                if len(i) > 2:
                    strip_i = ''.join(i)
                    d2 = EncodeBrackets(i)

                    for j in (d2['en_1']):
                        strip_i = strip_i.replace(j, '')
                    for j in (d2['en_2']):
                        strip_i = strip_i.replace(j, '')
                    for j in (d2['en_3']):
                        strip_i = strip_i.replace(j, '')

                    diff_len = len(i) - len(strip_i)
                    _strip_i = replace_all_blank(strip_i)
                    cmp_i = i.lower().strip('"')
                    skip = False
                    if cmp_i.startswith('#'):
                        skip = True
                    if is_skip_underline and strip_i.find('_') > -1:
                        skip = True
                    # if not line_content.strip().startswith('text ') or line_content.strip().find(i) != 5:
                    #     skip = True
                    if is_path_or_dir_string(cmp_i):
                        skip = True
                    if skip:
                        continue
                    i = i[1:-1]
                    i = replace_unescaped_quotes(i)
                    i = i.replace("\\'", "'")
                    if is_open_filter:
                        if len(_strip_i) < filter_length:
                            # log_print(len(strip_i),i)
                            continue
                        e.add(i)
                        is_add = True
                    else:
                        e.add(i)
                        is_add = True
        if is_add:
            continue
        d = EncodeBracketContent(line_content, "'", "'")
        if 'oriList' in d.keys() and len(d['oriList']) > 0:
            for i in d['oriList']:
                if len(i) > 2:
                    strip_i = ''.join(i)
                    d2 = EncodeBrackets(i)

                    for j in (d2['en_1']):
                        strip_i = strip_i.replace(j, '')
                    for j in (d2['en_2']):
                        strip_i = strip_i.replace(j, '')
                    for j in (d2['en_3']):
                        strip_i = strip_i.replace(j, '')

                    diff_len = len(i) - len(strip_i)
                    _strip_i = replace_all_blank(strip_i)
                    cmp_i = i.lower().strip("'")
                    skip = False
                    if cmp_i.startswith('#'):
                        skip = True
                    if is_skip_underline and _strip_i.find('_') > -1:
                        skip = True
                    # if not line_content.strip().startswith('text ') or line_content.strip().find(i) != 5:
                    #     skip = True
                    if is_path_or_dir_string(cmp_i):
                        skip = True
                    if skip:
                        continue
                    i = i[1:-1]
                    i = replace_unescaped_quotes(i)
                    i = i.replace("\\'", "'")
                    if is_open_filter:
                        if len(_strip_i) < filter_length:
                            # log_print(len(strip_i),i)
                            continue
                        e.add(i)
                    else:
                        e.add(i)
    return e


def CreateEmptyFileIfNotExsit(p):
    if (p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    paths = os.walk(p + '/../../', topdown=False)

    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if (i[len(p + '/../../'):][:3] == 'tl\\'):
                continue
            if (file_name.endswith("rpy") == False):
                continue
            target = p + i[len(p + '/../../'):]
            targetDir = os.path.dirname(target)
            if os.path.exists(targetDir) == False:
                pathlib.Path(targetDir).mkdir(parents=True, exist_ok=True)
            if os.path.isfile(target) == False:
                open(target, 'w').close()


def WriteExtracted(p, extractedSet, is_open_filter, filter_length, is_gen_empty, is_skip_underline, is_py2):
    if (p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    index = p.rfind('tl\\')
    if index == -1:
        index = p.rfind('tl/')
    if (index == -1):
        log_print(p + ' no tl found!')
        return
    index2 = p.find('\\', index + 3)
    if index2 == -1:
        index2 = p.find('/', index + 3)
    if (index2 == -1):
        log_print(p + ' no tl found2!')
        return
    tl = p[index + 3:index2]
    paths = os.walk(p, topdown=False)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if (file_name.endswith("rpy") == False):
                continue
            target = p + '../../' + i[len(p):]
            if os.path.isfile(target) == False:
                log_print(target + " not exists skip!")
                continue

            e = ExtractFromFile(target, is_open_filter, filter_length, is_skip_underline, is_py2)
            eDiff = e - extractedSet
            if len(eDiff) > 0:
                f = io.open(i, 'a+', encoding='utf-8')
                f.write('\ntranslate ' + tl + ' strings:\n')
                lock.acquire()
                global num
                num_str = str(num)
                num = num + 1
                lock.release()
                tm = str(time.time())
                timestamp = '"old:' + tm + '_' + num_str + '"'
                head = '    old ' + timestamp + '\n    '
                timestamp = '"new:' + tm + '_' + num_str + '"'
                head = head + 'new ' + timestamp + '\n\n'
                f.write(head)
                for j in eDiff:
                    if not j.startswith('_p("""') and not j.endswith('""")'):
                        j = '"' + j + '"'
                    if not is_gen_empty:
                        writeData = '    old ' + j + '\n    new ' + j + '\n'
                    else:
                        writeData = '    old ' + j + '\n    new ' + '""' + '\n'
                    f.write(writeData + '\n')
                f.close()
            extractedSet = e | extractedSet
            log_print(target + ' extract success!')


def GetHeaderPath(p):
    dic = dict()
    index = p.rfind('game/')
    if index == -1:
        index = p.rfind('game//')
    if index == -1:
        dic['header'] = ''
        return dic
    header = p[:index]
    if os.path.exists(header + 'renpy'):
        dic['header'] = header + 'game/'
        dirname = os.path.dirname(p) + '/'
        subPath = dirname[len(header) + len('game/'):]
        dic['subPath'] = subPath
        dic['fileName'] = os.path.basename(p)
        return dic
    else:
        dic['header'] = ''
        return dic


def ExtractWriteFile(p, tl_name, is_open_filter, filter_length, is_gen_empty, global_e, is_skip_underline):
    dic = GetHeaderPath(p)
    header = dic['header']
    if (header == ''):
        log_print(p + ' not in game path!')
        return set()
    subPath = dic['subPath']
    fileName = dic['fileName']
    targetDir = header + 'tl/' + tl_name + '/' + subPath
    target = targetDir + fileName
    if (os.path.exists(targetDir) == False):
        try:
            os.makedirs(targetDir)
        except FileExistsError:
            pass
    if (os.path.isfile(target) == False):
        open(target, 'w').close()
    is_py2 = is_python2_from_game_dir(targetDir.rstrip('/').rstrip('\\') + '/../../../')
    e = ExtractFromFile(p, is_open_filter, filter_length, is_skip_underline, is_py2)
    extractedSet = ExtractFromFile(target, False, 9999, is_skip_underline, is_py2)
    eDiff = e - extractedSet
    if len(eDiff) > 0:
        f = io.open(target, 'a+', encoding='utf-8')
        f.write('\ntranslate ' + tl_name + ' strings:\n')
        lock.acquire()
        global num
        num_str = str(num)
        num = num + 1
        lock.release()
        tm = str(time.time())
        timestamp = '"old:' + tm + '_' + num_str + '"'
        head = '    old ' + timestamp + '\n    '
        timestamp = '"new:' + tm + '_' + num_str + '"'
        head = head + 'new ' + timestamp + '\n\n'
        f.write(head)
        for j in eDiff:
            if j in global_e:
                continue
            if not j.startswith('_p("""') and not j.endswith('""")'):
                j = '"' + j + '"'
            if not is_gen_empty:
                writeData = '    old ' + j + '\n    new ' + j + '\n'
            else:
                writeData = '    old ' + j + '\n    new ' + '""' + '\n'
            f.write(writeData + '\n')
        f.close()
    global_e = global_e | e
    global_e = global_e | extractedSet
    log_print(target + ' extracted success!')
    return global_e


def ExtractAllFilesInDir(dirName, is_open_filter, filter_length, is_gen_empty, is_skip_underline):
    is_py2 = is_python2_from_game_dir(dirName + '/../../../')
    CreateEmptyFileIfNotExsit(dirName)
    WriteExtracted(dirName, set(), is_open_filter, filter_length, is_gen_empty, is_skip_underline, is_py2)
    log_print('start removing repeated extraction, please waiting...')
    remove_repeat_extracted_from_tl(dirName, is_py2)
    cnt = 0
    get_extracted_set_list.clear()
    p = dirName
    if p[len(p) - 1] != '/' and p[len(p) - 1] != '\\':
        p = p + '/'
    paths = os.walk(p, topdown=False)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if file_name.endswith("rpy") == False:
                continue
            t = ExtractTlThread(i, is_py2, True)
            get_extracted_threads.append(t)
            cnt = cnt + 1
            t.start()
    while True:
        threads_len = len(get_extracted_threads)
        if threads_len > 0:
            for t in get_extracted_threads:
                if t.is_alive():
                    t.join()
                get_extracted_threads.remove(t)
        else:
            break
    get_extracted_set_list.clear()