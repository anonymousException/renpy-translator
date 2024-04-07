import json
import os.path

from bs4 import BeautifulSoup, NavigableString

from my_log import log_print
from renpy_translate import get_translated
from string_tool import EncodeBrackets, isAllPunctuations

last_write_html = None
last_translated_dic = None


def write_html_with_strings(p, strings, data):
    if strings is None:
        return
    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    for s in strings:
        b_tag = soup.new_tag("b",)
        b_tag.string = s
        soup.body.append(b_tag)
        soup.body.append(soup.new_tag("br"))
    if data is not None:
        data_div = soup.new_tag("div", id="data", style="display: none;")
        data_div.string = data
        soup.body.append(data_div)
    with open(p, "w", encoding='utf-8') as f:
        f.write(str(soup))
    global last_write_html
    last_write_html = p


def read_strings_from_html(p):
    if not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    b_tags = soup.find_all('b')
    data_div = soup.find(id='data')
    data = None
    if data_div is not None:
        data = data_div.string
    strings = [tag.get_text() for tag in b_tags]
    return strings, data


def read_strings_from_translated(p):
    if not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()
    l = []
    for i in lines:
        i = i.strip('\n')
        if len(i) > 0:
            l.append(i)
    return l


def get_translated_dic(html_path, translated_path):
    dic = dict()
    ori_strings, data = read_strings_from_html(html_path)
    if data is not None:
        data = json.loads(data)
    global last_translated_dic
    if ori_strings is None or len(ori_strings) == 0:
        last_translated_dic = None
        return None
    translated_strings = read_strings_from_translated(translated_path)
    if translated_strings is None or len(translated_strings) == 0:
        last_translated_dic = None
        return None
    if len(ori_strings) != len(translated_strings):
        log_print('Error:translated file does not match the html file')
        last_translated_dic = None
        return None
    if data is not None:
        for i, e in enumerate(data):
            translated_dic = dict()
            target = e['target']
            line = e['line']
            if 'd' not in e:
                dic[ori_strings[i]] = translated_strings[i]
                continue
            d = e['d']
            translated = translated_strings[i]
            translated_dic[target] = translated
            translated = get_translated(translated_dic, d)
            if translated is None:
                translated = ''
                encoded = d['encoded'].strip('"')
                if encoded in translated_dic:
                    translated = translated_dic[encoded]
                log_print(
                    f'{translated_path} Error in line:{str(i + 1)} row:{line}\n{target}\n{encoded}\n{translated}\nError')
            dic[ori_strings[i]] = translated
    else:
        for i, e in enumerate(ori_strings):
            dic[e] = translated_strings[i]
    last_translated_dic = dic
    return dic, data is not None


def plain_text_to_html(p, output_p, is_replace_special_symbols):
    ret = []
    l = read_strings_from_translated(p)
    for i, e in enumerate(l):
        dic = dict()
        target = e
        dic['target'] = target
        dic['original'] = e
        dic['current'] = e
        dic['line'] = i
        if is_replace_special_symbols:
            d = EncodeBrackets(e)
            if not isAllPunctuations(d['encoded'].strip('"')):
                target = d['encoded'].strip('"')
                dic['target'] = target
                dic['d'] = d
                l[i] = target
        ret.append(dic)
    data = json.dumps(ret)
    if not is_replace_special_symbols:
        data = None
    write_html_with_strings(output_p, l, data)
