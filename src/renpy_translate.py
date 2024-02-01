import gc
import string
import sys
import io
import os
import threading
import traceback

import torch

from my_log import log_print
import warnings

warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

translate_threads = []
clientDic = dict()

t_lock = threading.Lock()

class translateThread(threading.Thread):
    def __init__(self, threadID, client, p, lang_target, lang_source,batch_size):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client
        self.p = p
        self.lang_target = lang_target
        self.lang_source = lang_source
        self.batch_size = batch_size

    def run(self):
        try:
            if self.client in clientDic.values():
                t_lock.acquire()
            log_print(self.p + ' begin translate!')
            TranslateFile(self.client, self.p, self.lang_target, self.lang_source,self.batch_size)
            if self.client in clientDic.values():
                t_lock.release()
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)


def TranslateToList(cli, inList, lang_target, lang_source,batch_size):
    dic = dict()
    if cli in clientDic.values():
        texts = cli.translate(inList, target=lang_target, source=lang_source,verbose=True,batch_size = batch_size)
    else:
        texts = cli.translate(inList, target=lang_target, source=lang_source)
    gc.collect()
    torch.cuda.empty_cache()
    for i, e in enumerate(texts):
        if isinstance(e, str):
            dic[inList[i]] = e
        else:
            dic[inList[i]] = e.translatedText
    return dic


def EncodeBracketContent(s, bracketLeft, bracketRight, isAddSpace=False):
    start = -1
    end = 0
    cnt = 0
    i = 0
    dic = dict()
    dic["ori"] = s
    oriList = []
    if (bracketLeft != bracketRight):
        matchLeftCnt = 0
        matchRightCnt = 0
        while True:
            _len = len(s)
            if (i >= _len):
                if (matchLeftCnt != matchRightCnt and start != -1):
                    i = start + 1
                    matchLeftCnt = 0
                    matchRightCnt = 0
                    continue
                break
            if (s[i] == bracketLeft):
                matchLeftCnt = matchLeftCnt + 1
                if (i == 0):
                    start = i
                else:
                    if (s[i - 1] == '\\'):
                        i = i + 1
                        continue
                    else:
                        if (matchLeftCnt == (matchRightCnt + 1)):
                            start = i
            if (s[i] == bracketRight):
                if (i == 0):
                    continue
                else:
                    if (s[i - 1] == '\\'):
                        i = i + 1
                        continue
                    else:
                        matchRightCnt = matchRightCnt + 1
                        if (start != -1):
                            if (matchLeftCnt == matchRightCnt):
                                end = i
            if (start != -1 and end > start):
                if (matchLeftCnt != matchRightCnt):
                    continue
                replace = ''
                if (isAddSpace):
                    replace = ' ' + bracketLeft + str(cnt) + bracketRight + ' '
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
        dic['cnt'] = cnt
        dic['encoded'] = s
        dic['oriList'] = oriList
        return dic
    else:
        while True:
            _len = len(s)
            if (i >= _len):
                break
            if (s[i] == bracketLeft):
                if (i == 0):
                    start = i
                else:
                    if (s[i - 1] == '\\'):
                        i = i + 1
                        continue
                    else:
                        if (start > end):
                            end = i
                        else:
                            start = i
            if (start != -1 and end > start):
                replace = bracketLeft + str(cnt) + bracketRight
                ori = s[start:end + 1]
                oriList.append(ori)
                s = s[:start] + replace + s[end + 1:]
                i = start + len(replace) - 1
                cnt = cnt + 1
                start = -1
                end = 0
            i = i + 1
            dic['cnt'] = cnt
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
        if (i >= _len):
            break
        if (s[i] == bracketLeft):
            if (i == 0):
                start = i
            else:
                if (s[i - 1] == '\\'):
                    i = i + 1
                    continue
                else:
                    start = i
        if (s[i] == bracketRight):
            if (i == 0):
                continue
            else:
                if (s[i - 1] == '\\'):
                    i = i + 1
                    continue
                else:
                    if (start != -1):
                        end = i
        if (start != -1 and end > start):
            ori = s[start:end + 1]
            index = int(ori[1:len(ori) - 1])
            replace = l[index]
            oriList.append(ori)
            s = s[:start] + replace + s[end + 1:]
            i = start + len(replace) - 1
            cnt = cnt + 1
            start = -1
            end = 0
        i = i + 1
    dic['cnt'] = cnt
    dic['decoded'] = s
    dic['oriList'] = oriList
    return dic


def EncodeBrackets(s):
    dic = dict()
    d = EncodeBracketContent(s, '<', '>', True)
    # print(d['encoded'])
    d2 = EncodeBracketContent(d['encoded'], '{', '}', True)
    # print(d2['encoded'],d2['oriList'])
    d3 = EncodeBracketContent(d2['encoded'], '[', ']', True)
    # print(d3['encoded'],d3['oriList'])
    dic['encoded'] = d3['encoded']
    dic['en_1'] = d['oriList']
    dic['en_1_cnt'] = d['cnt']
    dic['en_2'] = d2['oriList']
    dic['en_2_cnt'] = d2['cnt']
    dic['en_3'] = d3['oriList']
    dic['en_3_cnt'] = d3['cnt']
    return dic


def DecodeBrackets(s, en_1, en_2, en_3):
    dic = dict()
    d4 = DecodeBracketContent(s, '[', ']', en_3)
    d5 = DecodeBracketContent(d4['decoded'], '{', '}', en_2)
    d6 = DecodeBracketContent(d5['decoded'], '<', '>', en_1)
    dic['decoded'] = d6["decoded"]
    dic['de_4'] = d4['oriList']
    dic['de_4_cnt'] = d4['cnt']
    dic['de_5'] = d5['oriList']
    dic['de_5_cnt'] = d5['cnt']
    dic['de_6'] = d6['oriList']
    dic['de_6_cnt'] = d6['cnt']
    return dic


def isAllPunctuations(s):
    punc = string.punctuation
    for i in s:
        if (i in punc):
            continue
        else:
            return False
    return True


def TranslateFile(client, p, lang_target, lang_source,batch_size):
    transList = []
    try:
        f = io.open(p, 'r+', encoding='utf-8')
    except:
        log_print(p + ' file not found')
        return
    _read = f.read()
    _read_line = _read.split('\n')
    isLastFiltered = False
    isNeedSkip = False
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
            if (_read_line[line_index - 1].strip()[4:] != _read_line[line_index].strip()[4:] and _read_line[
                                                                                                     line_index - 1].strip()[
                                                                                                 2:] != _read_line[
                line_index].strip()):
                continue
        else:
            isLastFiltered = False

        if line_index >0 and not _read_line[line_index - 1].strip().startswith('#') and not _read_line[line_index - 1].strip().startswith('old '):
            continue
        d = EncodeBracketContent(line_content, '"', '"')
        if ('oriList' in d.keys() and len(d['oriList']) > 0):
            # print(d['oriList'])
            for i in d['oriList']:
                d = EncodeBrackets(i)
                if (isAllPunctuations(d['encoded'].strip('"')) == False):
                    transList.append(d['encoded'].strip('"'))
                # dd = DecodeBrackets(
                #     d['encoded'], d['en_1'], d['en_2'], d['en_3'])
                # print(d['encoded'],dd)
    if (len(transList) == 0):
        log_print(p + ' translate skip!')
        return
    # for i in transList:
    #     threadLock.acquire()
    #     log_print(i)
    #     threadLock.release()
    trans_dic = TranslateToList(client, transList, lang_target, lang_source,batch_size)

    translated_line = []
    isLastFiltered = False
    isNeedSkip = False
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
            if (_read_line[line_index - 1].strip()[4:] != _read_line[line_index].strip()[4:] and _read_line[
                                                                                                     line_index - 1].strip()[
                                                                                                 2:] != _read_line[
                line_index].strip()):
                continue
        else:
            isLastFiltered = False
        if line_index >0 and not _read_line[line_index - 1].strip().startswith('#') and not  _read_line[line_index - 1].strip().startswith('old '):
            continue
        d = EncodeBracketContent(line_content, '"', '"')
        if ('oriList' in d.keys() and len(d['oriList']) > 0):
            for i in d['oriList']:
                d = EncodeBrackets(i)
                if (isAllPunctuations(d['encoded'].strip('"')) == True):
                    continue
                translated = trans_dic[d['encoded'].strip('"')]
                translated = translated.replace('\u200b', '')
                translated = translated.replace('\u200b1', '')
                translated = translated.replace('"', '\"')
                translated = translated.replace('【', '[')
                translated = translated.replace('】', ']')
                translated = translated.rstrip('\\')
                translated = '"' + translated + '"'
                try:
                    dd = DecodeBrackets(
                        translated, d['en_1'], d['en_2'], d['en_3'])
                    if d['en_1_cnt'] != dd['de_6_cnt'] or d['en_2_cnt'] != dd['de_5_cnt'] or d['en_3_cnt'] != dd[
                        'de_4_cnt']:
                        raise Exception('decoded error')
                    dd = dd['decoded']
                    dd = dd.replace('&gt;', '>')
                    dd = dd.replace('&#39;', "'")
                    dd = dd.replace('&quot;', '\"')
                    _read_line[line_index] = _read_line[line_index].replace(
                        i, dd)
                except:
                    log_print(
                        'Error in line:' + str(line_index) + ' '+ p + '\n' + i + '\n' + d['encoded'].strip('"') + ' Error' + '\n' + translated)

    f = io.open(p + '.bak', 'w', encoding='utf-8')
    f.write(_read)
    f.close()
    f = io.open(p, 'w', encoding='utf-8')
    for line_content in _read_line:
        f.write(line_content + '\n')
    f.close()
    log_print(p + ' translate success!')
