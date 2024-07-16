import re
import string
import collections


def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())


def split_strings(strings, max_length=5000):
    result = []
    current_string = []

    for string in strings:
        _len = 0
        for i in current_string:
            _len += len(i)
        if _len + len(string) <= max_length:
            current_string.append(string)
        else:
            result.append(current_string)
            current_string = [string]

    if current_string:
        result.append(current_string)
    return result


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
            if (s[i] == bracketRight and matchLeftCnt > 0):
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
                        if (start >= end and i - start > 1):
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
                i = i + 1
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
    d = EncodeBracketContent(s, '<', '>')
    # print(d['encoded'])
    d2 = EncodeBracketContent(d['encoded'], '{', '}')
    # print(d2['encoded'],d2['oriList'])
    d3 = EncodeBracketContent(d2['encoded'], '[', ']')
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


def encode_say_string(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("\n", "\\n")
    s = s.replace("\"", "\\\"")
    s = re.sub(r'(?<= ) ', '\\ ', s)
    return s


def replace_all_blank(value):
    result = re.sub('\\W+', '', value).replace("_", '')
    return result


def replace_unescaped_quotes(text):
    pattern = r'(?<!\\)"'
    replaced_text = re.sub(pattern, r'\\"', text)
    return replaced_text


def tail(filename, n):
    last_lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        last_lines = collections.deque(file, maxlen=n)
    return last_lines
