import threading

limit_time_span_dic = dict()
lock = threading.Lock()
count = 0
app_key = ""
rpm = 0
rps = 0
tpm = 0
model = ""
base_url = ""
proxies = None
time_out = 0
max_length = 0
openai_template_file = 'openai_template.json'


def translate(_app_key, _app_secret, source, target, _proxies, q):
    import io
    import os
    import threading
    import time
    import traceback

    import httpx
    import openai
    from openai import OpenAI
    import json
    import concurrent.futures

    class TranslateResponse:
        def __init__(self, ori, res):
            self.untranslatedText = ori
            self.translatedText = res

    def remove_upprintable_chars(s):
        return ''.join(x for x in s if x.isprintable())

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

    def init_openai_param():
        global openai_template_file
        global app_key, rpm, rps, tpm, model, base_url, proxies, time_out, max_length
        config_path = 'engine.txt'
        if not os.path.isfile(config_path):
            config_path = '../' + config_path
            openai_template_file = '../' + openai_template_file
        with open(config_path, 'r', encoding='utf-8') as json_file:
            loaded_data = json.load(json_file)
            base_url = ''
            if proxies is None:
                proxies = dict()
                proxies['https'] = None
            if 'openai_base_url' in loaded_data and len(loaded_data['openai_base_url']) > 0:
                base_url = loaded_data['openai_base_url']
            if 'time_out' not in loaded_data or len(loaded_data['openai_model']) == 0:
                if loaded_data['openai_model'].startswith('gpt-3.5'):
                    loaded_data['time_out'] = 120
                else:
                    loaded_data['time_out'] = 240
            if 'max_length' not in loaded_data or len(loaded_data['max_length']) == 0:
                loaded_data['max_length'] = 5000
            app_key = loaded_data['key']
            rpm = int(loaded_data['rpm'])
            rps = int(loaded_data['rps'])
            tpm = int(loaded_data['tpm'])
            model = loaded_data['openai_model']
            time_out = int(loaded_data['time_out'])
            max_length = int(loaded_data['max_length'])
            proxies = proxies['https']

    def spilt_half_and_re_translate(data, source, target):
        half = int(len(data) / 2)
        data_1 = data[:half]
        data_2 = data[half:]
        dic1 = translate_limit(data_1, source, target)
        dic2 = translate_limit(data_2, source, target)
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

    def translate_limit(data, source, target):
        global count, lock
        try:
            if base_url is not None and base_url != "" and len(base_url) > 0:
                client = OpenAI(
                    # This is the default and can be omitted
                    api_key=app_key,
                    base_url=base_url,
                    http_client=httpx.Client(
                        proxies=proxies,
                        transport=httpx.HTTPTransport(local_address="0.0.0.0"))
                )
            else:
                client = OpenAI(
                    # This is the default and can be omitted
                    api_key=app_key,
                    http_client=httpx.Client(
                        proxies=proxies,
                        transport=httpx.HTTPTransport(local_address="0.0.0.0"))
                )
            lock.acquire()
            t_minute = time.strftime("%H:%M")
            if t_minute not in limit_time_span_dic:
                limit_time_span_dic[t_minute] = 1
            else:
                limit_time_span_dic[t_minute] = limit_time_span_dic[t_minute] + 1
            # RPM (requests per minute)
            if limit_time_span_dic[t_minute] > rpm:
                print("RPM (requests per minute) exceed,start waiting 65 seconds")
                time.sleep(65)
                limit_time_span_dic.clear()
                count = 0

            t_second = int(time.time())
            if t_second not in limit_time_span_dic:
                limit_time_span_dic[t_second] = 1
            else:
                limit_time_span_dic[t_second] = limit_time_span_dic[t_second] + 1
            # RPS (requests per second)
            if limit_time_span_dic[t_second] >= rps:
                time.sleep(1)
            ori_dic = dict()
            for i, e in enumerate(data):
                ori_dic[i] = e
            js = json.dumps(ori_dic)
            count = count + len(js) * 1.5
            if count >= tpm:
                print("TOKEN LIMITS exceed. start waiting 70 seconds...")
                time.sleep(70)
                limit_time_span_dic.clear()
                count = 0
                lock.release()
                return translate_limit(data, source, target)
            lock.release()
            try:
                source_template = '#SOURCE_LANGUAGE_ID!@$^#'
                target_template = '#TARGET_LANGAUGE_ID!@$^#'
                js_template = '#JSON_DATA_WAITING_FOR_TRANSLATE_ID!@$^#'
                messages = []
                if os.path.isfile(openai_template_file):
                    f = io.open(openai_template_file, 'r', encoding='utf-8')
                    template = f.read()
                    f.close()
                    template = template.replace(source_template, source)
                    template = template.replace(target_template, target)
                    try:
                        messages = json.loads(template)
                    except:
                        pass
                if not messages:
                    print(f'{openai_template_file} is not a valid json template, please check the template file!')
                    return None
                for message in messages:
                    for key, value in message.items():
                        if js_template in value:
                            message[key] = value.replace(js_template, js)

                if source is not None and source != 'AUTO':
                    pass
                else:
                    source = ''
                chat_completion = client.with_options(timeout=time_out, max_retries=2).chat.completions.create(
                    messages=messages,
                    model=model,
                    # temperature=1.3
                    # response_format={"type": "json_object"},
                )
            except openai.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)  # an underlying Exception, likely raised within httpx.
                print(e)
                print(data)
                return None
            except openai.RateLimitError as e:
                print("A 429 status code was received; we should back off a bit.")
                print(e)
                print(data)
                return None
            except openai.APIStatusError as e:
                print(f"Another non-200-range status code was received:{e.status_code} {e.response}")
                print(e)
                print(data)
                return None
            try:
                result = json.loads(str(chat_completion.choices[0].message.content))
                print('part translation success,still in progress,please waiting...')
                # print(result)
            except Exception as e:
                if len(data) < 5:
                    print('openai return an error json format')
                    print(chat_completion)
                    print(data)
                    return None
                else:
                    return spilt_half_and_re_translate(data, source, target)
            dic = dict()
            l = []
            if len(result) != len(ori_dic):
                if len(data) < 5:
                    print('translated result can not match the untranslated contents')
                    print(result)
                    print(ori_dic)
                    return None
                else:
                    return spilt_half_and_re_translate(data, source, target)

            isCorrectId = True
            for i in result:
                try:
                    num = int(remove_upprintable_chars(i))
                except Exception as e:
                    isCorrectId = False
                    break
            if not isCorrectId:
                if len(data) < 5:
                    print('open ai return an error id')
                    print(result)
                    print(ori_dic)
                    return None
                else:
                    return spilt_half_and_re_translate(data, source, target)
            for i in result:
                num = int(remove_upprintable_chars(i))
                if num in ori_dic:
                    translateResponse = TranslateResponse(ori_dic[num], result[i])
                    l.append(translateResponse)
            dic['l'] = l
            return dic
        except Exception as e:
            msg = traceback.format_exc()
            print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')

    global limit_time_span_dic
    try:
        init_openai_param()
    except Exception as e:
        print('failed to init openai parameter, please check your config in engine settings for OpenAI')
        return []
    app_key = _app_key
    result_arrays = split_strings(q, max_length)
    ret_l = []
    to_do = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for idx, result_array in enumerate(result_arrays):
            # print(result_array)
            # l = self.translate_limit(result_array, source, target)
            if len(result_array) == 0:
                continue
            future = executor.submit(translate_limit, result_array, source, target)
            to_do.append(future)
            # for i in l:
            #     ret_l.append(i)
    for future in concurrent.futures.as_completed(to_do):
        result = future.result()
        if result is not None and 'l' in result.keys():
            ret_l = ret_l + result['l']
    limit_time_span_dic.clear()
    return ret_l


# ret = translate('app_key', None, 'English', 'Chinese', {'http': 'http://localhost:10809'},
#                 ['OpenAI is the best translation service'])
# print(ret)
