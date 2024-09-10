# define the max length for each request
def get_max_length():
    return 4800

# if your api can not input untranslated list such as ['Hello','World']
# but can only accept single text input like 'Hello World'
# use this api , the example is baidu.py


def translate_single(app_key, app_secret, source, target, proxies, text):
    # return translated_text
    pass


# otherwise,use this api
# notice that, any other function call should not be out of this function
# you can directly include other function in this function ,like tranlate_deepl , otherwise will cause NameError
def translate_queue(app_key, app_secret, source, target, proxies, q):
    # write import inside the function , otherwise will cause NameError
    import json
    import requests
    import traceback
    import deepl
    class TranslateResponse:
        def __init__(self, res):
            self.detected_source_lang = res.detected_source_lang
            self.translatedText = res.text

    def translate_deepl(token, source, target, proxies, q):
        translator = deepl.Translator(token, proxy=proxies)
        result = translator.translate_text(q, target_lang=target, source_lang=source)
        l = []
        for i, e in enumerate(result):
            translateResponse = TranslateResponse(e)
            dic = dict()
            dic['untranslatedText'] = q[i]
            dic['translatedText'] = translateResponse.translatedText
            l.append(dic)
        # you are supposed to return a list
        # the list item should be a dict which contains two keys
        # 'untranslatedText' : the original text
        # 'translatedText : the translated text
        return l

    return translate_deepl(app_key, source, target, proxies, q)


# source = ["Deepl is the best translation service.", "How are you"]
# result = tranlate_queue('app_key', None, 'EN', 'ZH', None, source)
# print(result)
