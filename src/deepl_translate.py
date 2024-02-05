import concurrent.futures
import deepl

from src.my_log import log_print


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
                future = executor.submit(self.translate_limit, result_array, cnt, source, target)
                cnt = cnt + 1
                to_do.append(future)
                # for i in l:
                #     ret_l.append(i)
        dic = dict()
        for future in concurrent.futures.as_completed(to_do):
            result = future.result()
            dic[result['id']] = result['l']
        sorted_dict_items = sorted(dic.items())
        for key, value in sorted_dict_items:
            for i in value:
                ret_l.append(i)
        return ret_l

    def translate_limit(self, data, id, source, target):
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