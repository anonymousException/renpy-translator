import json
import string
import sys
import io
import os
import threading
import traceback

from pygtrans import Translate, ApiKeyTranslate

from my_log import log_print
from deepl_translate import DeeplTranslate
from openai_translate import OpenAITranslate
from custom_translate import CustomTranslate
from translator_translate import TranslatorTranslate
from youdao_translate import YoudaoTranslate
from string_tool import *

language_header = 'supported_language/'
custom_header = 'custom_engine/'

engineList = ['Google(Free)', 'Google(Token Required)', 'YouDao(Token Required)', 'DeepL(Token Required)',
              'OpenAI(Token Required)', 'Alibaba(Free)', 'ModernMt(Free)', 'Bing(Free)', 'Lingvanex(Free)',
              'CloudTranslation(Free)', 'YouDao(Free)', 'Caiyun(Free)']

engineDic = {engineList[0]: {'url': 'https://cloud.google.com/translate/docs/quickstarts', 'key_edit': False,
                             'secret_edit': False, 'target': 'google.target.rst', 'source': 'google.source.rst'},
             engineList[1]: {'url': 'https://cloud.google.com/translate/docs/quickstarts', 'key_edit': True,
                             'secret_edit': False, 'target': 'google.target.rst', 'source': 'google.source.rst'},
             engineList[10]: {'url': 'https://ai.youdao.com/doc.s#guide', 'key_edit': False,
                              'secret_edit': False, 'target': 'youdao_free.target.rst',
                              'source': 'youdao_free.source.rst'},
             engineList[2]: {'url': 'https://ai.youdao.com/doc.s#guide', 'key_edit': True,
                             'secret_edit': True, 'target': 'youdao.target.rst', 'source': 'youdao.source.rst'},
             engineList[3]: {
                 'url': 'https://www.deepl.com/account/?utm_source=github&utm_medium=github-python-readme',
                 'key_edit': True, 'secret_edit': False, 'target': 'deepl.target.rst', 'source': 'deepl.source.rst'},
             engineList[4]: {'url': 'https://platform.openai.com/api-keys', 'key_edit': True,
                             'secret_edit': False, 'target': 'openai.target.rst', 'source': 'openai.source.rst'},
             engineList[5]: {'url': 'https://translate.alibaba.com', 'key_edit': False,
                             'secret_edit': False, 'target': 'alibaba.target.rst', 'source': 'alibaba.source.rst'},
             engineList[6]: {'url': 'https://www.modernmt.com/translate', 'key_edit': False,
                             'secret_edit': False, 'target': 'modernMt.target.rst', 'source': 'modernMt.source.rst'},
             engineList[7]: {'url': 'https://www.bing.com/Translator', 'key_edit': False,
                             'secret_edit': False, 'target': 'bing.target.rst', 'source': 'bing.source.rst'},
             engineList[8]: {'url': 'https://lingvanex.com/demo', 'key_edit': False,
                             'secret_edit': False, 'target': 'lingvanex.target.rst', 'source': 'lingvanex.source.rst'},
             engineList[9]: {'url': 'https://www.cloudtranslation.com/#/translate', 'key_edit': False,
                             'secret_edit': False, 'target': 'cloudTranslation.target.rst',
                             'source': 'cloudTranslation.source.rst'},
             engineList[11]: {'url': 'https://fanyi.caiyunapp.com/', 'key_edit': False,
                              'secret_edit': False, 'target': 'caiyun.target.rst', 'source': 'caiyun.source.rst'},
             }

translate_threads = []
translate_lock = threading.Lock()
client_openai = None


class translateThread(threading.Thread):
    def __init__(self, threadID, p, lang_target, lang_source, is_open_multi_thread, is_gen_bak,local_glossary,is_translate_current,is_skip_translated):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.p = p
        self.lang_target = lang_target
        self.lang_source = lang_source
        self.is_open_multi_thread = is_open_multi_thread
        self.is_gen_bak = is_gen_bak
        self.local_glossary = local_glossary
        self.is_translate_current = is_translate_current
        self.is_skip_translated = is_skip_translated

    def run(self):
        if not self.is_open_multi_thread:
            translate_lock.acquire()
        try:
            log_print(self.p + ' begin translate!')
            TranslateFile(self.p, self.lang_target, self.lang_source, self.is_gen_bak,self.local_glossary,self.is_translate_current,self.is_skip_translated)
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')
        if not self.is_open_multi_thread:
            translate_lock.release()


def TranslateToList(cli, inList, lang_target, lang_source,fmt = 'text'):
    dic = dict()
    if cli.__class__.__name__ != 'Translate':
        texts = cli.translate(inList, target=lang_target, source=lang_source)
    else:
        texts = cli.translate(inList, target=lang_target, source=lang_source,fmt = fmt)
    if isinstance(texts, list):
        for i, e in enumerate(texts):
            if cli.__class__.__name__ == 'OpenAITranslate':
                if hasattr(e, 'untranslatedText'):
                    dic[e.untranslatedText] = e.translatedText
            else:
                dic[inList[i]] = e.translatedText
    else:
        raise Exception('translate error:' + str(texts))
    return dic

def init_client():
    proxies = None
    client = None
    customEngineDic = dict()
    if os.path.isfile('custom.txt'):
        f = io.open('custom.txt', 'r', encoding='utf-8')
        customEngineDic = json.load(f)
        f.close()
    if os.path.isfile('proxy.txt'):
        with open('proxy.txt', 'r') as json_file:
            loaded_data = json.load(json_file)
            if loaded_data['enable']:
                proxies = {'https': loaded_data['proxy']}
                os.environ['HTTPS_PROXY'] = loaded_data['proxy']
                os.environ['HTTP_PROXY'] = loaded_data['proxy']
                if 'NO_PROXY' in os.environ.keys():
                    del os.environ['NO_PROXY']
            else:
                if 'HTTPS_PROXY' in os.environ.keys():
                    del os.environ['HTTPS_PROXY']
                if 'HTTP_PROXY' in os.environ.keys():
                    del os.environ['HTTP_PROXY']
                os.environ['NO_PROXY'] = '*'
    if os.path.isfile('engine.txt'):
        with open('engine.txt', 'r') as json_file:
            loaded_data = json.load(json_file)
            if loaded_data['engine'] == engineList[0]:
                client = Translate(fmt='text', proxies=proxies)
            elif loaded_data['engine'] == engineList[1]:
                client = ApiKeyTranslate(fmt='text', proxies=proxies, api_key=loaded_data['key'])
            elif loaded_data['engine'] == engineList[2]:
                client = YoudaoTranslate(app_key=loaded_data['key'], app_secret=loaded_data['secret'], proxies=proxies)
            elif loaded_data['engine'] == engineList[3]:
                client = DeeplTranslate(app_key=loaded_data['key'], proxies=proxies)
            elif loaded_data['engine'] == engineList[4]:
                base_url = ''
                if proxies == None:
                    proxies = dict()
                    proxies['https'] = None
                if 'openai_base_url' in loaded_data and len(loaded_data['openai_base_url']) > 0:
                    base_url = loaded_data['openai_base_url']
                global client_openai
                if client_openai is None:
                    client_openai = OpenAITranslate(app_key=loaded_data['key'], rpm=loaded_data['rpm'],
                                                    rps=loaded_data['rps'], tpm=loaded_data['tpm'],
                                                    model=loaded_data['openai_model'], base_url=base_url,
                                                    proxies=proxies['https'])
                else:
                    client_openai.reset(app_key=loaded_data['key'], rpm=loaded_data['rpm'], rps=loaded_data['rps'],
                                        tpm=loaded_data['tpm'], model=loaded_data['openai_model'], base_url=base_url,
                                        proxies=proxies['https'])
                client = client_openai
            elif loaded_data['engine'] == engineList[5]:
                client = TranslatorTranslate('alibaba', proxies=None)
            elif loaded_data['engine'] == engineList[6]:
                client = TranslatorTranslate('modernMt', proxies=None)
            elif loaded_data['engine'] == engineList[7]:
                client = TranslatorTranslate('bing', proxies=None)
            elif loaded_data['engine'] == engineList[8]:
                client = TranslatorTranslate('lingvanex', proxies=None)
            elif loaded_data['engine'] == engineList[9]:
                client = TranslatorTranslate('cloudTranslation', proxies=None)
            elif loaded_data['engine'] == engineList[10]:
                client = TranslatorTranslate('youdao', proxies=None)
            elif loaded_data['engine'] == engineList[11]:
                client = TranslatorTranslate('caiyun', proxies=None)
            elif loaded_data['engine'] in customEngineDic.keys():
                config = customEngineDic[loaded_data['engine']]
                client = CustomTranslate(custom_header + config['file_name'], loaded_data['key'], loaded_data['secret'],
                                         proxies, config['is_queue'])
            else:
                log_print('engine.txt' + ' file format error!')
                msg = traceback.format_exc()
                log_print(msg)
                return client
    else:
        client = Translate(fmt='text', proxies=proxies)
    return client

def TranslateFile(p, lang_target, lang_source, is_gen_bak,local_glossary,is_translate_current,is_skip_translated):
    client = init_client()
    if client is None:
        return
    transList = []
    ret, unmatch_cnt, p = get_rpy_info(p)
    if len(ret) == 0:
        log_print(p + ' unable to get translated info')
        return
    for dic in ret:
        original = dic['original']
        current = dic['current']
        if is_translate_current:
            target = current
        else:
            target = original
        if is_skip_translated and original != current:
            continue
        if local_glossary is not None and len(local_glossary) > 0:
            for original,replace in local_glossary.items():
                target = target.replace(original, replace)
        d = EncodeBrackets(target)
        if (isAllPunctuations(d['encoded'].strip('"')) == False):
            transList.append(d['encoded'].strip('"'))
    if client.__class__.__name__ == 'Translate' and local_glossary is not None and len(local_glossary) > 0:
        fmt = 'html'
    else:
        fmt = 'text'
    trans_dic = TranslateToList(client, transList, lang_target, lang_source,fmt=fmt)
    if len(transList) == 0:
        log_print(p + ' translate skip!')
        return
    f = io.open(p, 'r', encoding='utf-8')
    _read_lines = f.readlines()
    f.close()
    if is_gen_bak:
        f = io.open(p + '.bak', 'w', encoding='utf-8')
        f.writelines(_read_lines)
        f.close()
    for dic in ret:
        line = dic['line'] - 1
        ori_line = dic['ori_line'] - 1
        original = dic['original']
        current = dic['current']
        if is_translate_current:
            target = current
        else:
            target = original
        if is_skip_translated and original != current:
            continue
        ori_target = target
        if local_glossary is not None and len(local_glossary) > 0:
            for original, replace in local_glossary.items():
                target = target.replace(original, replace)
        translated = get_translated(trans_dic,target)
        if translated is None:
            d = EncodeBrackets(target)
            log_print(
                p + ' Error in line:' + str(line) + ' ' + '\n' + target + '\n' + d['encoded'].strip(
                    '"') + ' Error')
        else:
            target = ori_target
            if is_translate_current:
                _read_lines[line] =  _read_lines[line].replace(target, translated)
            else:
                _read_lines[line] = '    ' + _read_lines[ori_line].replace(target, translated).lstrip().lstrip('#').lstrip()
                if _read_lines[line].startswith('    old '):
                    _read_lines[line] = _read_lines[line].replace('    old ','    new ',1)

    f = io.open(p, 'w', encoding='utf-8')
    f.writelines(_read_lines)
    f.close()
    log_print(p + ' translate success!')


def get_translated(trans_dic,target):
    try:
        d = EncodeBrackets(target)
        if (isAllPunctuations(d['encoded'].strip('"')) == False):
            translated = trans_dic[d['encoded'].strip('"')]
            translated = translated.replace('\u200b', '')
            translated = translated.replace('\u200b1', '')
            translated = translated.replace('"', '\\"')
            translated = translated.replace('【', '[')
            translated = translated.replace('】', ']')
            translated = translated.rstrip('\\')
            dd = DecodeBrackets(
                translated, d['en_1'], d['en_2'], d['en_3'])
            if d['en_1_cnt'] != dd['de_6_cnt'] or d['en_2_cnt'] != dd['de_5_cnt'] or d['en_3_cnt'] != \
                    dd[
                        'de_4_cnt']:
                raise Exception('decoded error')
            dd = dd['decoded']
            dd = dd.replace('&gt;', '>')
            dd = dd.replace('&#39;', "'")
            dd = dd.replace('&quot;', '\\"')
            dd = dd.replace('\n', '\\n')
            return dd
    except:
        return None


def get_rpy_info(p):
    infoList = []
    try:
        f = io.open(p, 'r', encoding='utf-8')
    except:
        log_print(p + ' file not found')
        return infoList, 0, p
    try:
        size = os.path.getsize(p)
        _read = f.read()
        f.close()
    except:
        f.close()
        return infoList, 0, p
    _read_line = _read.split('\n')
    isLastFiltered = False
    isNeedSkip = False
    isVoice = False
    unmatch_cnt = 0
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
            # if (_read_line[line_index - 1].strip()[4:] != _read_line[line_index].strip()[4:] and _read_line[
            #                                                                                          line_index - 1].strip()[
            #                                                                                      2:] != _read_line[
            #     line_index].strip()):
            #     continue
        else:
            isLastFiltered = False
        if not isVoice:
            if line_index > 0 and not _read_line[line_index - 1].strip().startswith('#') and not _read_line[
                line_index - 1].strip().startswith('old '):
                continue
        if (line_content.strip().lstrip('#').strip().startswith('voice ')):
            isVoice = True
            continue
        d = EncodeBracketContent(line_content, '"', '"')
        if ('oriList' in d.keys() and len(d['oriList']) > 0):
            # print(d['oriList'])
            for i, e in enumerate(d['oriList']):
                if (isAllPunctuations(d['encoded'].strip('"')) == False):
                    target_index = line_index - 1
                    if isVoice:
                        target_index = target_index -1
                    if line_content.strip().startswith('new '):
                        d_o = EncodeBracketContent(_read_line[target_index].strip()[4:], '"', '"')
                    else:
                        d_o = EncodeBracketContent(_read_line[target_index].strip(), '"', '"')
                    original = ''
                    if ('oriList' in d_o.keys() and len(d_o['oriList']) > 0):
                        original = d_o['oriList'][i].strip('"')
                    is_match = True
                    if original != e.strip('"') and e.strip('"')!='':
                        unmatch_cnt = unmatch_cnt + 1
                        is_match = False
                    dic = dict()
                    dic['original'] = original
                    dic['current'] = e.strip('"')
                    dic['ori_line'] = target_index + 1
                    dic['line'] = line_index + 1
                    start = line_index - 2
                    if isVoice:
                        start = start - 2
                        isVoice = False
                    if line_content.strip().startswith('new '):
                        start = line_index
                    j = 0
                    end = start - 5
                    if end < 0:
                        end = -1
                    for j in range(start, end, -1):
                        if _read_line[j].strip().startswith('#'):
                            break
                    dic['refer'] = ''
                    if j != 0:
                        dic['refer'] = _read_line[j].strip('#')
                    dic['is_match'] = is_match
                    infoList.append(dic)
    # sorted(infoList, key=lambda x: x['line'])
    return infoList, unmatch_cnt, p
