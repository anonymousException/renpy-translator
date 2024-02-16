#-*- coding: utf-8
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

extract_threads = []

class extractThread (threading.Thread):
    def __init__(self, threadID, p,tl_name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.p = p
        self.tl_name = tl_name
    def run(self):
        try:
            log_print(self.p + ' begin extract!')
            ExtractWriteFile(self.p,self.tl_name)
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
def replace_all_blank(value):
    """
    去除value中的所有标点符号、空格、换行、下划线等
    :param value: 需要处理的内容
    :return: 返回处理后的内容
    """
    # \W 表示匹配非数字字母下划线
    result = re.sub('\\W+', '', value).replace("_", '')
    return result


def EncodeBracketContent(s, bracketLeft, bracketRight, isAddSpace=False):
    start = -1
    end = 0
    cnt = 0
    i = 0
    dic = dict()
    dic["ori"] = s
    oriList = []
    if(bracketLeft != bracketRight):
        matchLeftCnt = 0
        matchRightCnt = 0
        while True:
            _len = len(s)
            if(i >= _len):
                if(matchLeftCnt != matchRightCnt and start!=-1):
                    i = start + 1
                    matchLeftCnt = 0
                    matchRightCnt = 0
                    continue
                break
            if(s[i] == bracketLeft):
                matchLeftCnt = matchLeftCnt + 1
                if(i == 0):
                    start = i
                else:
                    if(s[i - 1] == '\\'):
                        i = i + 1
                        continue
                    else:
                        if(matchLeftCnt == (matchRightCnt + 1)):
                            start = i
            if(s[i] == bracketRight):
                if(i == 0):
                    continue
                else:
                    if(s[i - 1] == '\\'):
                        i = i + 1
                        continue
                    else:
                        matchRightCnt = matchRightCnt +1
                        if(start != -1):
                            if(matchLeftCnt == matchRightCnt):
                                end = i
            if(start != -1 and end > start):
                if(matchLeftCnt != matchRightCnt):
                    continue
                replace = ''
                if(isAddSpace):
                    replace = ' ' + bracketLeft  + str(cnt)  + bracketRight + ' '
                else:
                    replace = bracketLeft + str(cnt) + bracketRight
                ori = s[start:end + 1]
                oriList.append(ori)
                s = s[:start] + replace + s[end + 1:]
                i = start + len(replace) - 1
                cnt = cnt + 1
                start = -1
                end = 0
            i = i + 1
        dic['encoded'] = s
        dic['oriList'] = oriList
        return dic
    else:
        while True:
            _len = len(s)
            if(i >= _len):
                break
            if(s[i] == bracketLeft):
                if(i == 0):
                    start = i
                else:
                    if(s[i - 1] == '\\'):
                        i = i + 1
                        continue
                    else:
                        if(start > end):
                            end = i
                        else:
                            start = i
            if(start != -1 and end > start):
                replace = bracketLeft + str(cnt) + bracketRight
                ori = s[start:end + 1]
                oriList.append(ori)
                s = s[:start] + replace + s[end + 1:]
                i = start + len(replace) - 1
                cnt = cnt + 1
                start = -1
                end = 0
            i = i + 1
            dic['encoded'] = s
            dic['oriList'] = oriList
        return dic


def DecodeBracketContent(s, bracketLeft, bracketRight, l):
    start = -1
    end = 0
    cnt = 0
    i = 0
    dic = dict()
    dic["ori"] = s
    oriList = []
    while True:
        _len = len(s)
        if(i >= _len):
            break
        if(s[i] == bracketLeft):
            if(i == 0):
                start = i
            else:
                if(s[i - 1] == '\\'):
                    i = i + 1
                    continue
                else:
                    start = i
        if(s[i] == bracketRight):
            if(i == 0):
                continue
            else:
                if(s[i - 1] == '\\'):
                    i = i + 1
                    continue
                else:
                    if(start != -1):
                        end = i
        if(start != -1 and end > start):

            ori = s[start:end + 1]
            index = int(ori[1:len(ori) - 1])
            # print(l[index])
            replace = l[index]
            oriList.append(ori)
            s = s[:start] + replace + s[end + 1:]
            i = start + len(replace) - 1
            cnt = cnt + 1
            start = -1
            end = 0
        i = i + 1
    dic['decoded'] = s
    dic['oriList'] = oriList
    return dic


def EncodeBrackets(s):
    dic = dict()
    d = EncodeBracketContent(s, '<', '>', False)
    # log_print(d['encoded'])
    d2 = EncodeBracketContent(d['encoded'], '{', '}', False)
    # log_print(d2['encoded'],d2['oriList'])
    d3 = EncodeBracketContent(d2['encoded'], '[', ']', False)
    # log_print(d3['encoded'],d3['oriList'])
    dic['encoded'] = d3['encoded']
    dic['en_1'] = d['oriList']
    dic['en_2'] = d2['oriList']
    dic['en_3'] = d3['oriList']
    return dic


def DecodeBrackets(s, en_1, en_2, en_3):
    d4 = DecodeBracketContent(s, '[', ']', en_3)
    d5 = DecodeBracketContent(d4['decoded'], '{', '}', en_2)
    d6 = DecodeBracketContent(d5['decoded'], '<', '>', en_1)
    return d6["decoded"]


def ExtractFromFile(p, isOpenFilter):
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
        if(isOpenFilter):
            if(line_content.strip().startswith('#') or len(line_content.strip()) == 0):
                continue
            if(line_content.strip().startswith('label ')):
                continue
            if(line_content.strip().startswith('define ')):
                continue
            # if(line_content.strip().startswith('default ')):
            # 	continue
        # log_print(line_content)
        d = EncodeBracketContent(line_content, '"', '"')
        if('oriList' in d.keys() and len(d['oriList']) > 0):
            for i in d['oriList']:
                if(len(i) > 2):
                    if(isOpenFilter):
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
                        if((' ' in strip_i.strip()) == False and ('.' in strip_i.strip('.')) == False and (',' in strip_i.strip(',')) == False):
                            continue
                        elif(len(_strip_i) < 8):
                            # log_print(len(strip_i),i)
                            continue
                        cmp_i = i.lower().strip('"')
                        suffix_list = ['.ogg', '.webp', '.png', '.ttf', '.otf', '.webm', '.svg', '.gif', '.jpg', '.wav',
                                       '.mp3']
                        skip = False
                        if cmp_i.startswith('#'):
                            skip = True
                        for suffix in suffix_list:
                            if cmp_i.endswith(suffix) == False:
                                continue
                            else:
                                skip = True
                                break
                        if skip == False:
                            i = i.replace('\\\'', "'")
                            e.add(i)
                    else:
                        e.add(i)
    return e


def CreateEmptyFileIfNotExsit(p):
    if(p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    paths = os.walk(p + '/../../')

    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if(i[len(p + '/../../'):][:3] == 'tl\\'):
                continue
            if(file_name.endswith("rpy") == False):
                continue
            target = p + i[len(p + '/../../'):]
            targetDir = os.path.dirname(target)
            if os.path.exists(targetDir) == False:
                pathlib.Path(targetDir).mkdir(parents=True, exist_ok=True)
            if os.path.isfile(target) == False:
                open(target, 'w').close()


def GetExtractedSet(p):
    if(p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    e = set()
    paths = os.walk(p)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if(file_name.endswith("rpy") == False):
                continue
            extracted = ExtractFromFile(i, False)
            e = e | extracted
    return e


def WriteExtracted(p, extractedSet):
    if(p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
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
    paths = os.walk(p)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if(file_name.endswith("rpy") == False):
                continue
            target = p + '../../' + i[len(p):]
            if os.path.isfile(target) == False:
                log_print(target + " not exists skip!")
                continue

            e = ExtractFromFile(target, True)
            eDiff = e - extractedSet
            if(len(eDiff) > 0):
                f = io.open(i, 'a+', encoding='utf-8')
                f.write('\ntranslate '+ tl+' strings:\n')
                rdm = str(random.random())
                tm = str(time.time())
                timestamp = '"old:' + tm + '_' + rdm + '"'
                head = '    old ' + timestamp + '\n    '
                timestamp = '"new:' + tm + '_' + rdm + '"'
                head = head + 'new ' + timestamp + '\n\n'
                f.write(head)
                for j in eDiff:
                    writeData = '    old ' + j + '\n    new ' + j + '\n'
                    f.write(writeData + '\n')
                f.close()
            extractedSet = e | extractedSet
            log_print(target + ' extract success!')

def GetHeaderPath(p):
    dic = dict()
    index = p.rfind('game/')
    if(index == -1):
        index = p.rfind('game//')
    if(index==-1):
        dic['header'] = ''
        return dic
    header = p[:index]
    if(os.path.exists(header+'renpy')):
        dic['header'] = header + 'game/'
        dirname = os.path.dirname(p) + '/'
        subPath = dirname[len(header)+len('game/'):]
        dic['subPath'] = subPath
        dic['fileName'] = os.path.basename(p)
        return dic
    else:
        dic['header'] = ''
        return dic

def ExtractWriteFile(p,tl_name):
    dic = GetHeaderPath(p)
    header = dic['header']
    if(header ==''):
        log_print(p + ' not in game path!')
        return dic
    subPath = dic['subPath']
    fileName = dic['fileName']
    targetDir = header + 'tl/' + tl_name + '/' + subPath
    target = targetDir+ fileName
    if(os.path.exists(targetDir) == False):
        os.makedirs(targetDir)
    if(os.path.isfile(target) == False):
        open(target, 'w').close()
    e = ExtractFromFile(p,True)
    extractedSet = ExtractFromFile(target, True)
    eDiff = e - extractedSet
    if(len(eDiff) > 0):
        f = io.open(target, 'a+', encoding='utf-8')
        f.write('\ntranslate '+ tl_name +' strings:\n')
        timestamp = '"old:' + str(time.time()) + '"'
        head = '    old ' + timestamp + '\n    '
        timestamp = '"new:' + str(time.time()) + '"'
        head = head + 'new ' + timestamp + '\n\n'
        f.write(head)
        for j in eDiff:
            writeData = '    old ' + j + '\n    new ' + j + '\n'
            f.write(writeData + '\n')
        f.close()
    extractedSet = e | extractedSet
    log_print(target +' extracted success!')


def ExtractAllFilesInDir(dirName):
    CreateEmptyFileIfNotExsit(dirName)
    ret = GetExtractedSet(dirName)
    WriteExtracted(dirName, ret)
