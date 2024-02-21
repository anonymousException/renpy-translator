import concurrent.futures
import os
import traceback

import deepl

from my_log import log_print
from string_tool import split_strings


class TranslateResponse:
    def __init__(self, res):
        self.detected_source_lang = res.detected_source_lang
        self.translatedText = res.text


class DeeplTranslate(object):
    def __init__(self, app_key, proxies=None):
        self.app_key = app_key
        self.translator = deepl.Translator(app_key, proxy=proxies)

    def translate(self, q, source, target):
        result_arrays = split_strings(q, 4800)
        ret_l = []
        to_do = []
        cnt = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for idx, result_array in enumerate(result_arrays):
                # print(result_array)
                # l = self.translate_limit(result_array, source, target)
                if len(result_array) == 0:
                    continue
                future = executor.submit(self.translate_limit, result_array, cnt, source, target)
                cnt = cnt + 1
                to_do.append(future)
                # for i in l:
                #     ret_l.append(i)
        dic = dict()
        for future in concurrent.futures.as_completed(to_do):
            result = future.result()
            if result is not None:
                dic[result['id']] = result['l']
        sorted_dict_items = sorted(dic.items())
        for key, value in sorted_dict_items:
            for i in value:
                ret_l.append(i)
        return ret_l

    def translate_limit(self, data, id, source, target):
        try:
            if source == "AUTO":
                source = None
            result = self.translator.translate_text(
                data, target_lang=target, source_lang=source)
            dic = dict()
            l = []
            for i in result:
                translateResponse = TranslateResponse(i)
                l.append(translateResponse)
            dic['l'] = l
            dic['id'] = id
            return dic
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')