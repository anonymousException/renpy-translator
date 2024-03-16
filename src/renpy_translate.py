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
    def __init__(self, threadID, p, lang_target, lang_source, is_open_multi_thread, is_gen_bak):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.p = p
        self.lang_target = lang_target
        self.lang_source = lang_source
        self.is_open_multi_thread = is_open_multi_thread
        self.is_gen_bak = is_gen_bak

    def run(self):
        if not self.is_open_multi_thread:
            translate_lock.acquire()
        try:
            log_print(self.p + ' begin translate!')
            TranslateFile(self.p, self.lang_target, self.lang_source, self.is_gen_bak)
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')
        if not self.is_open_multi_thread:
            translate_lock.release()


def TranslateToList(cli, inList, lang_target, lang_source):
    dic = dict()
    texts = cli.translate(inList, target=lang_target, source=lang_source)
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

def TranslateFile(p, lang_target, lang_source, is_gen_bak):
    client = init_client()
    if client is None:
        return
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
        if line_index > 0 and not _read_line[line_index - 1].strip().startswith('#') and not _read_line[
            line_index - 1].strip().startswith('old '):
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
    trans_dic = TranslateToList(client, transList, lang_target, lang_source)

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
        if line_index > 0 and not _read_line[line_index - 1].strip().startswith('#') and not _read_line[
            line_index - 1].strip().startswith('old '):
            continue
        d = EncodeBracketContent(line_content, '"', '"')
        if ('oriList' in d.keys() and len(d['oriList']) > 0):
            for i in d['oriList']:
                d = EncodeBrackets(i)
                if (isAllPunctuations(d['encoded'].strip('"')) == True):
                    continue
                if d['encoded'].strip('"') not in trans_dic:
                    log_print(
                        'Error in line:' + str(line_index) + ' ' + p + '\n' + i + '\n' + d['encoded'].strip(
                            '"') + ' Error')
                    continue
                translated = trans_dic[d['encoded'].strip('"')]
                translated = translated.replace('\u200b', '')
                translated = translated.replace('\u200b1', '')
                translated = translated.replace('"', '\\"')
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
                    dd = dd.replace('&quot;', '\\"')
                    dd = dd.replace('\n', '\\n')
                    _read_line[line_index] = _read_line[line_index].replace(
                        i, dd)
                except:
                    log_print(
                        'Error in line:' + str(line_index) + ' ' + p + '\n' + i + '\n' + d['encoded'].strip(
                            '"') + ' Error' + '\n' + translated)

    if is_gen_bak:
        f = io.open(p + '.bak', 'w', encoding='utf-8')
        f.write(_read)
        f.close()
    f = io.open(p, 'w', encoding='utf-8')
    for line_content in _read_line:
        f.write(line_content + '\n')
    f.close()
    log_print(p + ' translate success!')
