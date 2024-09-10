import io
import os
from my_log import log_print, log_refresh
from string_tool import split_strings
import concurrent.futures
import traceback
import json
import requests
import string
import sys
import threading
import uuid
import hashlib
import time
from importlib import reload


def run_dynamic_code_from_file(file_path, function_name, *args, **kwargs):
    f = io.open(file_path, 'r', encoding='utf-8')
    code = f.read()
    f.close()
    return run_dynamic_code(code, function_name, *args, **kwargs)


def run_dynamic_code(code, function_name, *args, **kwargs):
    exec(code)
    try:
        function = locals()[function_name]
    except Exception:
        return None
    return function(*args, **kwargs)


class TranslateResponse:
    def __init__(self, ori, res):
        self.untranslatedText = ori
        self.translatedText = res


class CustomTranslate(object):
    def __init__(self, file_name, app_key, app_secret, proxies, is_queue):
        self.file_name = file_name
        self.proxies = proxies
        self.app_key = app_key
        self.app_secret = app_secret
        self.is_queue = is_queue

    def translate(self, q, source, target):
        try:
            log_refresh()
            ret = run_dynamic_code_from_file(self.file_name, 'translate', self.app_key, self.app_secret,
                                             source, target, self.proxies, q)
            if ret is not None:
                log_refresh()
                return ret
            max_length = run_dynamic_code_from_file(self.file_name, 'get_max_length')
            if max_length is None:
                max_length = 4800
            result_arrays = split_strings(q, max_length)
            ret_l = []
            to_do = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for idx, result_array in enumerate(result_arrays):
                    # print(result_array)
                    # l = self.translate_limit(result_array, source, target)
                    if len(result_array) == 0:
                        continue
                    future = executor.submit(self.translate_limit, result_array, source, target, self.is_queue)
                    to_do.append(future)
                    # for i in l:
                    #     ret_l.append(i)
            for future in concurrent.futures.as_completed(to_do):
                result = future.result()
                if result is not None and 'l' in result.keys():
                    ret_l = ret_l + result['l']
            log_refresh()
            return ret_l
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            return []

    def translate_limit(self, q, source, target, is_queue):
        try:
            dic = dict()
            l = []
            if not is_queue:
                for i in q:
                    # the function name should be 'translate' with 2 parameters:
                    # 1.app_key
                    # 2.app_secret
                    # 3.source_language
                    # 4.target_language
                    # 5.proxies
                    # 6.untranslatedText
                    ret = run_dynamic_code_from_file(self.file_name, 'translate_single', self.app_key, self.app_secret,
                                                     source, target, self.proxies, i)
                    if ret is not None:
                        if len(ret) > 0:
                            if (ret == i):
                                log_print(i + '\ntranslate return the original content')
                            else:
                                translateResponse = TranslateResponse(i, ret)
                                l.append(translateResponse)
                        else:
                            log_print(i + '\ntranslate fail')
                    else:
                        log_print(i + '\ntranslate fail')
            else:
                # the function name should be 'translate' with 2 parameters:
                # 1.app_key
                # 2.app_secret
                # 3.source_language
                # 4.target_language
                # 5.proxies
                # 6.untranslatedTextList
                ret = run_dynamic_code_from_file(self.file_name, 'translate_queue', self.app_key, self.app_secret,
                                                 source,
                                                 target, self.proxies, q)
                if ret is None:
                    raise Exception('run_dynamic_code_from_file return None , please check your code')
                for i in ret:
                    translateResponse = TranslateResponse(i['untranslatedText'], i['translatedText'])
                    l.append(translateResponse)
            dic['l'] = l
            return dic
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')
