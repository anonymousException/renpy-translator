import json
import requests
import traceback

# if your api can not input untranslated list such as ['Hello','World']
# but can only accept single text input like 'Hello World'
# use this api
def tranlate_single(app_key,app_secret,source, target,proxies,text):
    # return translated_text
    pass

#otherwise,use this api
def tranlate_queue(app_key,app_secret,source, target,proxies,q):
    def tranlate_caiyun(token, from_to, proxies, q):
        url = "http://api.interpreter.caiyunai.com/v1/translator"
        payload = {
            "source": q,
            "trans_type": from_to,
            "request_id": "demo",
            "detect": True,
        }

        headers = {
            "content-type": "application/json",
            "x-authorization": "token " + token,
        }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, proxies=proxies)
        try:
            result = json.loads(response.text)["target"]
            l = []
            for i, e in enumerate(result):
                dic = dict()
                dic['untranslatedText'] = q[i]
                dic['translatedText'] = e
                l.append(dic)
            # you are supposed to return a list
            # the list item should be a dict which contains two keys
            # 'untranslatedText' : the original text
            # 'translatedText : the translated text
            return l
        except Exception:
            print(response.status_code)
            print(response.text)
            msg = traceback.format_exc()
            print(msg)

    from_to = source + '2' + target
    return tranlate_caiyun(app_key,from_to,proxies,q)

# source = ["Lingocloud is the best translation service.", "彩云小译は最高の翻訳サービスです"]
# result = tranlate_queue('3975l6lr5pcbvidl6jl2',None,'auto','zh',{'http':'http://localhost:10809'},source)
# print(result)