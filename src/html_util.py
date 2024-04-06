import os.path

from bs4 import BeautifulSoup, NavigableString

from my_log import log_print

last_write_html = None
last_translated_dic = None


def write_html_with_strings(p, strings):
    if strings is None:
        return
    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    for s in strings:
        p_tag = soup.new_tag("p")
        p_tag.string = s
        soup.body.append(p_tag)

    with open(p, "w", encoding='utf-8') as f:
        f.write(str(soup))
    global last_write_html
    last_write_html = p


def read_strings_from_html(p):
    if not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    p_tags = soup.find_all('p')
    strings = [tag.get_text() for tag in p_tags]
    return strings


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
    ori_strings = read_strings_from_html(html_path)
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
    for i, e in enumerate(ori_strings):
        dic[e] = translated_strings[i]
    last_translated_dic = dic
    return dic
