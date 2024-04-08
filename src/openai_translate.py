import os
import threading
import time
import traceback

import httpx
import openai
from openai import OpenAI
import json
import concurrent.futures
from openai.types import Model, ModelDeleted

from my_log import log_print
from string_tool import remove_upprintable_chars, split_strings

# "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"
limit_time_span_dic = dict()


class TranslateResponse:
    def __init__(self, ori, res):
        self.untranslatedText = ori
        self.translatedText = res


class OpenAITranslate(object):
    lock = threading.Lock()
    count = 0

    def __init__(self, app_key, rpm, rps, tpm, model, base_url, time_out, proxies=None):
        self.app_key = app_key
        self.rpm = int(rpm)
        self.rps = int(rps)
        self.tpm = int(tpm)
        self.model = model
        self.base_url = base_url
        self.proxies = proxies
        self.timeout = int(time_out)

    def reset(self, app_key, rpm, rps, tpm, model, base_url, time_out, proxies=None):
        self.app_key = app_key
        self.rpm = int(rpm)
        self.rps = int(rps)
        self.tpm = int(tpm)
        self.model = model
        self.base_url = base_url
        self.proxies = proxies
        self.timeout = time_out

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
        limit_time_span_dic.clear()
        return ret_l

    def spilt_half_and_re_translate(self, data, source, target):
        half = int(len(data) / 2)
        data_1 = data[:half]
        data_2 = data[half:]
        dic1 = self.translate_limit(data_1, source, target)
        dic2 = self.translate_limit(data_2, source, target)
        dic = dict()
        l = []
        if dic1 is not None and 'l' in dic1.keys():
            l = dic1['l']
        if dic2 is not None and 'l' in dic2.keys():
            l = l + dic2['l']
        if len(l) < 0:
            return None
        dic['l'] = l
        return dic

    def translate_limit(self, data, source, target):
        try:
            if self.base_url is not None and self.base_url != "" and len(self.base_url) > 0:
                client = OpenAI(
                    # This is the default and can be omitted
                    api_key=self.app_key,
                    base_url=self.base_url,
                    http_client=httpx.Client(
                        proxies=self.proxies,
                        transport=httpx.HTTPTransport(local_address="0.0.0.0"))
                )
            else:
                client = OpenAI(
                    # This is the default and can be omitted
                    api_key=self.app_key,
                    http_client=httpx.Client(
                        proxies=self.proxies,
                        transport=httpx.HTTPTransport(local_address="0.0.0.0"))
                )
            self.lock.acquire()
            t_minute = time.strftime("%H:%M")
            if t_minute not in limit_time_span_dic:
                limit_time_span_dic[t_minute] = 1
            else:
                limit_time_span_dic[t_minute] = limit_time_span_dic[t_minute] + 1
            # RPM (requests per minute)
            if limit_time_span_dic[t_minute] > self.rpm:
                log_print("RPM (requests per minute) exceed,start waiting 65 seconds")
                time.sleep(65)
                limit_time_span_dic.clear()
                self.count = 0

            t_second = int(time.time())
            if t_second not in limit_time_span_dic:
                limit_time_span_dic[t_second] = 1
            else:
                limit_time_span_dic[t_second] = limit_time_span_dic[t_second] + 1
            # RPS (requests per second)
            if limit_time_span_dic[t_second] >= self.rps:
                time.sleep(1)
            ori_dic = dict()
            for i, e in enumerate(data):
                ori_dic[i] = e
            js = json.dumps(ori_dic)
            self.count = self.count + len(js) * 1.5
            if self.count >= self.tpm:
                log_print("TOKEN LIMITS exceed. start waiting 70 seconds...")
                time.sleep(70)
                limit_time_span_dic.clear()
                self.count = 0
                self.lock.release()
                return self.translate_limit(data, source, target)
            self.lock.release()
            try:
                if source is not None and source != 'AUTO':
                    source_lang_setup = f'You will receive a piece of {source} text in JSON dictionary format'
                    role_setup = 'You are a translation API that receives dictionary-type data in JSON format and returns dictionary-type results in JSON format'
                    format_requirement = 'do not consider that we are chatting or greeting me and simply reply to me with the translation in the same format as the original'
                    prompt = f'{role_setup}. {source_lang_setup}, where the key is the line number and the value is the content of the corresponding line. Please translate it into {target} according to the following requirements: \n' + \
                             '1. first read through the whole text, determine the type of text content and select the appropriate translation style before starting the translation; \n' + \
                             '2. use the homophonic translation for names of people and places consistently; \n' + \
                             '3. polish translation results to make them accurate and natural; \n' + \
                             '4. do not change or convert punctuation marks; \n' + \
                             f'5. {format_requirement}, which is an example of the format: \n' + \
                             'Me: {"1": "Contents of line 1", "2": "Contents of line 2", "3": "Contents of line 3"} \n' + \
                             'You: {"1": "Translation result for line 1", "2": "Translation result for line 2", "3": "Translation result for line 3"} \n' + \
                             f'Next you will receive the text that needs to be translated into {target}. \n' + \
                             f'{js}'
                    # prompt = f'You are a meticulous translator who translates any given content.Remember that json:{js} Be faithful or accurate in translation.Make the translation readable or intelligible. Be elegant or natural in translation.Make sure each translated text returned in original order.Translate the content from {source} into {target}.'
                    chat_completion = client.with_options(timeout=self.timeout, max_retries=2).chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        model=self.model,
                        # response_format={"type": "json_object"},
                    )
                else:
                    source_lang_setup = f'You will receive a piece of text in JSON dictionary format'
                    role_setup = 'You are a translation API that receives dictionary-type data in JSON format and returns dictionary-type results in JSON format'
                    format_requirement = 'do not consider that we are chatting or greeting me and simply reply to me with the translation in the same format as the original'
                    prompt = f'{role_setup}. {source_lang_setup}, where the key is the line number and the value is the content of the corresponding line. Please translate it into {target} according to the following requirements: \n' + \
                             '1. first read through the whole text, determine the type of text content and select the appropriate translation style before starting the translation; \n' + \
                             '2. use the homophonic translation for names of people and places consistently; \n' + \
                             '3. polish translation results to make them accurate and natural; \n' + \
                             '4. do not change or convert punctuation marks; \n' + \
                             f'5. {format_requirement}, which is an example of the format: \n' + \
                             'Me: {"1": "Contents of line 1", "2": "Contents of line 2", "3": "Contents of line 3"} \n' + \
                             'You: {"1": "Translation result for line 1", "2": "Translation result for line 2", "3": "Translation result for line 3"} \n' + \
                             f'Next you will receive the text that needs to be translated into {target}. \n' + \
                             f'{js}'
                    # prompt = f'You are a meticulous translator who translates any given content.Remember that json:{js} Be faithful or accurate in translation.Make the translation readable or intelligible. Be elegant or natural in translation.Never merge the translation result.Make sure each translated text returned in original order.Translate the content into {target}.'
                    chat_completion = client.with_options(timeout=self.timeout, max_retries=2).chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        model=self.model,
                        # response_format={"type": "json_object"},
                    )
            except openai.APIConnectionError as e:
                log_print("The server could not be reached")
                log_print(e.__cause__)  # an underlying Exception, likely raised within httpx.
                log_print(e)
                log_print(data)
                return None
            except openai.RateLimitError as e:
                log_print("A 429 status code was received; we should back off a bit.")
                log_print(e)
                log_print(data)
                return None
            except openai.APIStatusError as e:
                log_print(f"Another non-200-range status code was received:{e.status_code} {e.response}")
                log_print(e)
                log_print(data)
                return None
            try:
                result = json.loads(str(chat_completion.choices[0].message.content))
                log_print('part translation success,still in progress,please waiting...')
                # log_print(result)
            except Exception as e:
                if len(data) < 5:
                    log_print('openai return an error json format')
                    log_print(chat_completion)
                    log_print(data)
                    return None
                else:
                    return self.spilt_half_and_re_translate(data, source, target)
            dic = dict()
            l = []
            if len(result) != len(ori_dic):
                if len(data) < 5:
                    log_print('translated result can not match the untranslated contents')
                    log_print(result)
                    log_print(ori_dic)
                    return None
                else:
                    return self.spilt_half_and_re_translate(data, source, target)

            isCorrectId = True
            for i in result:
                try:
                    num = int(remove_upprintable_chars(i))
                except Exception as e:
                    isCorrectId = False
                    break
            if not isCorrectId:
                if len(data) < 5:
                    log_print('open ai return an error id')
                    log_print(result)
                    log_print(ori_dic)
                    return None
                else:
                    return self.spilt_half_and_re_translate(data, source, target)
            for i in result:
                num = int(remove_upprintable_chars(i))
                if num in ori_dic:
                    translateResponse = TranslateResponse(ori_dic[num], result[i])
                    l.append(translateResponse)
            dic['l'] = l
            return dic
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')
