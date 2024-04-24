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
from string_tool import remove_upprintable_chars, EncodeBracketContent, EncodeBrackets, replace_all_blank, \
    replace_unescaped_quotes

extract_threads = []

lock = threading.Lock()

num = 0


class extractThread(threading.Thread):
    def __init__(self, threadID, p, tl_name, dirs, tl_dir, is_open_filter, filter_length, is_gen_empty):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.p = p
        self.tl_name = tl_name
        self.dirs = dirs
        self.tl_dir = tl_dir
        self.is_open_filter = is_open_filter
        self.filter_length = filter_length
        self.is_gen_empty = is_gen_empty

    def run(self):
        try:
            if self.tl_dir is not None and os.path.exists(self.tl_dir):
                self.tl_dir = self.tl_dir.rstrip('/')
                self.tl_dir = self.tl_dir.rstrip('\\')
                if self.tl_name is not None and len(self.tl_name) > 0:
                    ori_tl = os.path.basename(self.tl_dir)
                    self.tl_dir = self.tl_dir[:-len(ori_tl)] + self.tl_name
                log_print(self.tl_dir + ' begin extract!')
                ExtractAllFilesInDir(self.tl_dir, self.is_open_filter, self.filter_length, self.is_gen_empty)
            else:
                if self.p is not None:
                    self.p = self.p.replace('\\', '/')
                    log_print(self.p + ' begin extract!')
                    ExtractWriteFile(self.p, self.tl_name, self.is_open_filter, self.filter_length, self.is_gen_empty,
                                     set())
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
                                                            self.is_gen_empty, global_e)
                                global_e = global_e | ret_e

        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


def ExtractFromFile(p, is_open_filter, filter_length):
    e = set()
    f = io.open(p, 'r+', encoding='utf-8')
    _read = f.read()
    f.close()
    # print(_read)
    _read_line = _read.split('\n')
    is_in_condition_switch = False
    for line_content in _read_line:
        if 'ConditionSwitch(' in line_content:
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
        if (is_open_filter):
            if cmp_line_content.startswith('label '):
                continue
            if cmp_line_content.startswith('define '):
                continue
            # if(line_content.strip().startswith('default ')):
            # 	continue
        # log_print(line_content)
        suffix_list = ['.ogg', '.webp', '.png', '.ttf', '.otf', '.webm', '.svg', '.gif', '.jpg', '.wav',
                       '.mp3']
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
                    # if not line_content.strip().startswith('text ') or line_content.strip().find(i) != 5:
                    #     skip = True
                    for suffix in suffix_list:
                        if cmp_i.endswith(suffix) == False:
                            continue
                        else:
                            skip = True
                            break
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
                    # if not line_content.strip().startswith('text ') or line_content.strip().find(i) != 5:
                    #     skip = True
                    for suffix in suffix_list:
                        if cmp_i.endswith(suffix) == False:
                            continue
                        else:
                            skip = True
                            break
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


def GetExtractedSet(p):
    if (p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    e = set()
    paths = os.walk(p, topdown=False)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if (file_name.endswith("rpy") == False):
                continue
            extracted = ExtractFromFile(i, False, 9999)
            both = e & extracted
            if len(both) > 0:
                f = io.open(i, 'r', encoding='utf-8')
                lines = f.readlines()
                f.close()
                for j in both:
                    j = '"' + j + '"'
                    for index, line in enumerate(lines):
                        if line.startswith('    old ' + j):
                            lines[index] = '\n'
                            lines[index + 1] = '\n'
                f = io.open(i, 'w', encoding='utf-8')
                f.writelines(lines)
                f.close()

            e = e | extracted
    return e


def WriteExtracted(p, extractedSet, is_open_filter, filter_length, is_gen_empty):
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

            e = ExtractFromFile(target, is_open_filter, filter_length)
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


def ExtractWriteFile(p, tl_name, is_open_filter, filter_length, is_gen_empty, global_e):
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
    e = ExtractFromFile(p, is_open_filter, filter_length)
    extractedSet = ExtractFromFile(target, False, 9999)
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


def ExtractAllFilesInDir(dirName, is_open_filter, filter_length, is_gen_empty):
    CreateEmptyFileIfNotExsit(dirName)
    ret = GetExtractedSet(dirName)
    WriteExtracted(dirName, ret, is_open_filter, filter_length, is_gen_empty)
    ret = GetExtractedSet(dirName)
