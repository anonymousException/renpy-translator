import os

from my_log import log_print
from string_tool import split_strings
import concurrent.futures
import traceback
import translators as ts

class TranslateResponse:
    def __init__(self,ori,res):
        self.untranslatedText =ori
        self.translatedText = res

class TranslatorTranslate(object):
    """
    translate_text(query_text: str, translator: str = 'bing', from_language: str = 'auto', to_language: str = 'en', **kwargs) -> Union[str, dict]
        :param query_text: str, must.
        :param translator: str, default 'bing'.
        :param from_language: str, default 'auto'.
        :param to_language: str, default 'en'.
        :param if_use_preacceleration: bool, default False.
        :param **kwargs:
                :param is_detail_result: bool, default False.
                :param professional_field: str, default None. Support alibaba(), baidu(), caiyun(), cloudTranslation(), elia(), sysTran(), youdao(), volcEngine() only.
                :param timeout: float, default None.
                :param proxies: dict, default None.
                :param sleep_seconds: float, default 0.
                :param update_session_after_freq: int, default 1000.
                :param update_session_after_seconds: float, default 1500.
                :param if_use_cn_host: bool, default False. Support google(), bing() only.
                :param reset_host_url: str, default None. Support google(), yandex() only.
                :param if_check_reset_host_url: bool, default True. Support google(), yandex() only.
                :param if_ignore_empty_query: bool, default False.
                :param limit_of_length: int, default 20000.
                :param if_ignore_limit_of_length: bool, default False.
                :param if_show_time_stat: bool, default False.
                :param show_time_stat_precision: int, default 2.
                :param if_print_warning: bool, default True.
                :param lingvanex_mode: str, default 'B2C', choose from ("B2C", "B2B").
                :param myMemory_mode: str, default "web", choose from ("web", "api").
        :return: str or dict
    """
    def __init__(self,translator,proxies):
        self.translator = translator
        self.proxies = proxies

    def translate(self, q, source, target):
        result_arrays = split_strings(q, 4800)
        ret_l = []
        to_do = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for idx, result_array in enumerate(result_arrays):
                # print(result_array)
                # l = self.translate_limit(result_array, source, target)
                if len(result_array) == 0:
                    continue
                future = executor.submit(self.translate_limit, result_array, source, target)
                to_do.append(future)
                # for i in l:
                #     ret_l.append(i)
        for future in concurrent.futures.as_completed(to_do):
            result = future.result()
            if result is not None and 'l' in result.keys():
                ret_l = ret_l + result['l']
        return ret_l

    def translate_limit(self, q, source, target):
        try:
            dic = dict()
            l = []
            for i in q:
                ret = ts.translate_text(i, from_language= source,to_language =target,translator=self.translator, proxies=self.proxies)
                if len(ret) > 0:
                    if (ret == i):
                        log_print(i + '\ntranslate return the original content')
                    else:
                        translateResponse = TranslateResponse(i, ret)
                        l.append(translateResponse)
                else:
                    log_print(i +  '\ntranslate fail')
            dic['l'] = l
            return dic
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')