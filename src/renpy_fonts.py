# -*- coding: utf-8
import io
import shutil
import sys
import os
import time
import traceback

from my_log import log_print

font_style_tempalte_path = 'font_style_template.txt'


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
                    if 'font "' in e or "font '" in e:
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
            if (file_name.endswith("rpy") == False):
                continue
            if (i[len(p):len(p) + 3] == 'tl\\'):
                continue
            # print(i)
            d = ExtractStyleFontListFromFile(i)
            if len(d) > 0:
                ret_d.update(d)
    return ret_d


def ExtractFontContent(data):
    index = data.find('font "')
    if (index == -1):
        return data
    index2 = data[index + 6:].find('"') + index + 6 + 1
    return data[index:index2]


def GenGuiFontsOriginal(p, tl_name, font_path):
    if (p[len(p) - 1] != '/' and p[len(p) - 1] != '\\'):
        p = p + '/'
    guiPath = p + 'tl/' + tl_name + '/gui.rpy'
    # print(guiPath)
    appendMode = False
    _read = ''
    pythonBeginLine = 'translate ' + tl_name + ' python:'
    if (os.path.isfile(guiPath)):
        f = io.open(guiPath, 'r', encoding='utf-8')
        _read = f.read()
        f.close()
        if (pythonBeginLine in _read):
            appendMode = True
    result = ExtractStyleFontListFromDirectory(p)
    if (appendMode):
        f = io.open(guiPath, 'a+', encoding='utf-8')
        for key, value in result.items():
            if key in _read:
                continue
            f.write('\n')
            # content = 'translate ' + tl_name + ' ' + key + '\n'  +value['content'] +'    #' +value['font'].lstrip() + '\n' + value['font']
            fontLine = value['font']
            fontContent = ExtractFontContent(fontLine)
            replacedFont = fontLine.replace(fontContent, 'font gui.text_font')
            # print(replacedFont)
            content = 'translate ' + tl_name + ' ' + key + '\n' + value['content'] + '    #' + value[
                'font'].lstrip() + '\n    ' + replacedFont
            # print(value['file'])
            # print(content)
            f.write(content)
            f.write('\n')
        f.close()
        log_print(guiPath + ' generated append!')
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
        f = io.open(guiPath, 'w', encoding='utf-8')
        header = template
        # print(header)
        f.write(header)
        f.write('\n')
        for key, value in result.items():
            f.write('\n')
            # content = 'translate ' + tl_name + ' ' + key + '\n'  +value['content'] +'    #' +value['font'].lstrip() + '\n' + value['font']
            fontLine = value['font']
            fontContent = ExtractFontContent(fontLine)
            replacedFont = fontLine.replace(fontContent, 'font gui.text_font')
            # print(replacedFont)
            content = 'translate ' + tl_name + ' ' + key + '\n' + value['content'] + '    #' + value[
                'font'].lstrip() + '\n    ' + replacedFont
            # print(value['file'])
            # print(content)
            f.write(content)
            f.write('\n')
        f.close()
        log_print(guiPath + ' generated success!')


def GenGuiFonts(path, fp):
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
    GenGuiFontsOriginal(path[:index], tl, fp)

# path = 'F:/Games/RenPy/Outland-Wanderer-0.0.21-win/game'
# tl = 'schinese'
# fp = 'Source_Han_Serif_CN-Bold.otf'
# GenGuiFonts(path, tl, fp)
