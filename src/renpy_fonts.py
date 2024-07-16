# -*- coding: utf-8
import io
import re
import shutil
import sys
import os
import time
import traceback

from my_log import log_print

font_style_tempalte_path = 'font_style_template.txt'


def replace_font_content(text, new_content):
    pattern = r'\{font\s*=\s*.*?\}.*?\{/font\}'
    replacement = lambda m: re.sub(r'{font\s*=\s*.*?}', f'{{font={new_content}}}', m.group(0))
    return re.sub(pattern, replacement, text)


def ExtractDefineList(data):
    define_list = set()
    _read_line = data.split('\n')
    for idx, line in enumerate(_read_line):
        line = line.strip()
        if line.endswith('"'):
            line = line.strip('"')
        if line.endswith("'"):
            line = line.strip("'")
        if line.startswith('define '):
            suffix_list = ['.otf', '.ttf', '.ttc', '.otc', '.woff', '.woff2']
            for suffix in suffix_list:
                if line.endswith(suffix):
                    line = _read_line[idx].strip()
                    defined_var = line[7:line.find('=')].strip()
                    define_list.add(defined_var)
                    break
    return define_list

def ExtractStyleList(data):
    _read_line = data.split('\n')
    last_i = 0
    style_list = []
    # print(len(_read_line))
    _len = len(_read_line)
    if (_read_line[0].startswith('style ')):
        for i in range(0, len(_read_line)):
            if (i == 0):
                continue
            line = _read_line[i]
            if (len(line) > 0 and line[0] != ' '):
                style_list.append(_read_line[0:i])
                last_i = i
                break
    last_i = 0
    for i in range(0, _len):
        line = _read_line[i]
        # print(i,line)
        if (i < last_i):
            continue
        # print(i+1,line)
        if (line.startswith('style ')):
            if (last_i != 0):
                # print(last_i,i)
                style_list.append(_read_line[last_i:i])
                last_i = 0
            last_i = i
        elif (len(line) > 0 and line[0] != ' '):
            if (last_i != 0):
                # print(last_i,i)
                style_list.append(_read_line[last_i:i])
                last_i = 0
    # print(style_list)

    return style_list


def ExtractStyleFontList(data, file=None):
    dic = dict()
    for i in data:
        # print(i)
        # dic[i[0]] = i[1]
        # print(len(i))
        if len(i) > 1:
            content = ''
            flag = False
            font_line = ''
            for _i, e in enumerate(i):
                if _i != 0:
                    if 'font ' in e:
                        font_line = e
                        flag = True
                        continue
                    if len(e.strip()) > 0:
                        content = content + e.rstrip() + '\n'

            # print(content)
            if flag:
                d = dict()
                d['font'] = font_line
                d['content'] = content
                d['file'] = file
                dic[i[0]] = d
    return dic


def ExtractStyleFontListFromFile(p):
    f = io.open(p, 'r+', encoding='utf-8')
    _read = f.read()
    f.close()
    ret = ExtractStyleList(_read)
    # print(ret)
    # for i in ret:
    #     print(i)
    d = ExtractStyleFontList(ret, p)

    return d

def ExtractStyleFontListFromDirectory(p):
    if (p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    ret_d = dict()
    paths = os.walk(p, topdown=False)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if file_name.endswith("rpy") == False:
                continue
            if i[len(p):len(p) + 3] == 'tl\\':
                continue
            # print(i)
            d = ExtractStyleFontListFromFile(i)
            if len(d) > 0:
                ret_d.update(d)
    return ret_d


def ExtractFontContent(data):
    index = data.find('font ')
    if index == -1:
        return data
    return data[index:]


def GenGuiFontsOriginal(p, tl_name, font_path, is_rtl_enabled):
    if p[len(p) - 1] != '/' and p[len(p) - 1] != '\\':
        p = p + '/'
    guiPath = p + 'tl/' + tl_name + '/gui.rpy'
    # print(guiPath)
    appendMode = False
    _read = ''
    pythonBeginLine = 'translate ' + tl_name + ' python:'
    if os.path.isfile(guiPath):
        f = io.open(guiPath, 'r', encoding='utf-8')
        _read = f.read()
        f.close()
        if pythonBeginLine in _read:
            appendMode = True
    #result = ExtractStyleFontListFromDirectory(p)
    if appendMode:
        f = io.open(guiPath, 'r', encoding='utf-8')
        _lines = f.readlines()
        f.close()
        for idx,_line in enumerate(_lines):
            if 'tl_font_dic[' in _line:
                new_line = f'tl_font_dic["{tl_name}"] = "{font_path}", {str(is_rtl_enabled)}'
                _lines[idx] = new_line
                break
        f = io.open(guiPath, 'w', encoding='utf-8')
        f.writelines(_lines)
        f.close()
    else:
        game_fonts_path = p + '/fonts/'
        if os.path.exists(game_fonts_path) == False:
            os.mkdir(game_fonts_path)
        abs_font_path = font_path
        font_path = os.path.basename(font_path)
        if os.path.isfile(abs_font_path) == False:
            log_print('font:' + font_path + ' does not exist! skip generate ' + guiPath)
            return
        copy_font_path = game_fonts_path + font_path
        # noinspection PyBroadException
        try:
            shutil.copy(abs_font_path, copy_font_path)
            log_print('copy font file:' + abs_font_path + ' to ' + copy_font_path + ' success!')
        except Exception:
            msg = traceback.format_exc()
            log_print(msg)
            log_print('copy font file:' + abs_font_path + ' to ' + copy_font_path + ' fail!')
        f = io.open(font_style_tempalte_path, 'r', encoding='utf-8')
        template = f.read()
        f.close()
        template = template.replace('{tl_name}', tl_name)
        template = template.replace('{font_path}', 'fonts/' + font_path)
        if is_rtl_enabled:
            template = template.replace('{is_rtl_enabled}', 'True')
        else:
            template = template.replace('{is_rtl_enabled}', 'False')
        f = io.open(guiPath, 'w', encoding='utf-8')
        header = template
        # print(header)
        f.write(header)
        f.write('\n')
        # for key, value in result.items():
        #     f.write('\n')
        #     # content = 'translate ' + tl_name + ' ' + key + '\n'  +value['content'] +'    #' +value['font'].lstrip() + '\n' + value['font']
        #     fontLine = value['font']
        #     fontContent = ExtractFontContent(fontLine)
        #     replacedFont = fontLine.replace(fontContent, 'font gui.text_font')
        #     # print(replacedFont)
        #     content = 'translate ' + tl_name + ' ' + key + '\n' + value['content'] + '    #' + value[
        #         'font'].lstrip() + '\n' + replacedFont
        #     # print(value['file'])
        #     # print(content)
        #     f.write(content)
        #     f.write('\n')
        f.close()
        log_print(guiPath + ' generated success!')


def replace_tl_folder(full_tl_path, font_name):
    paths = os.walk(full_tl_path, topdown=False)
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            i = os.path.join(path, file_name)
            if file_name.endswith("rpy") == False:
                continue
            f = io.open(i, 'r', encoding='utf-8')
            lines = f.readlines()
            f.close()
            is_p = False
            for index, line in enumerate(lines):
                if line.strip().startswith('old _p("""'):
                    is_p = True
                if is_p:
                    if line.endswith('""")\n'):
                        is_p = False
                    continue
                if not '{font' in line:
                    continue
                if not line.strip().startswith('#') and not line.strip().startswith('old '):
                    data = replace_font_content(line, 'fonts/' + font_name)
                    lines[index] = data
            f = io.open(i, 'w', encoding='utf-8')
            f.writelines(lines)
            f.close()


def GenGuiFonts(path, fp, is_rtl_enabled):
    index = path.rfind('tl\\')
    if index == -1:
        index = path.rfind('tl/')
    if (index == -1):
        log_print(path + ' no tl found!')
        return
    index2 = path.find('\\', index + 3)
    if index2 == -1:
        index2 = path.find('/', index + 3)
    if (index2 == -1):
        log_print(path + ' no tl found2!')
        return
    tl = path[index + 3:index2]
    GenGuiFontsOriginal(path[:index], tl, fp, is_rtl_enabled)
    font_name = os.path.basename(fp)
    #replace_tl_folder(path[:index] + 'tl/' + tl, font_name)

# path = 'F:/Games/RenPy/Outland-Wanderer-0.0.21-win/game'
# tl = 'schinese'
# fp = 'Source_Han_Serif_CN-Bold.otf'
# GenGuiFonts(path, tl, fp)
