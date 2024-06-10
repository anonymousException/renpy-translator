import io
import json
import os.path
import subprocess
import threading

from bs4 import BeautifulSoup, NavigableString
from string_tool import EncodeBrackets, isAllPunctuations

last_write_html = None
last_translated_dic = None

_write_lock = threading.Lock()


def write_html_with_strings(p, strings, data):
    if strings is None:
        return
    _write_lock.acquire()
    if os.path.isfile(p):
        _strings, _data = read_strings_from_html(p)
        if data is not None:
            data = json.loads(data)
            _data = json.loads(_data)
            for i in _data:
                data.append(i)
            data = json.dumps(data)
            for i in _strings:
                strings.append(i)

    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    for s in strings:
        b_tag = soup.new_tag("h6", )
        b_tag.string = s
        soup.body.append(b_tag)
    if data is not None:
        data_div = soup.new_tag("div", id="data", style="display: none;")
        data_div.string = data
        soup.body.append(data_div)
    with open(p, "w", encoding='utf-8') as f:
        f.write(str(soup))
    global last_write_html
    last_write_html = p
    _write_lock.release()


def read_strings_from_html(p):
    if not os.path.isfile(p):
        return None, None
    with open(p, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    h6_tags = soup.find_all('h6')
    data_div = soup.find(id='data')
    data = None
    if data_div is not None:
        data = data_div.string
    strings = [tag.get_text() for tag in h6_tags]
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


def plain_text_to_html_from_list(l, output_p, is_replace_special_symbols):
    ret = []
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


def plain_text_to_html(p, output_p, is_replace_special_symbols):
    l = read_strings_from_translated(p)
    return plain_text_to_html_from_list(l, output_p, is_replace_special_symbols)


def open_directory_and_select_file(file_path):
    subprocess.run(["explorer", "/select,", os.path.normpath(file_path)])
