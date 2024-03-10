def tranlate_single(app_key,app_secret,source, target,proxies,text):
    import hashlib
    import traceback
    import urllib
    import random
    import json
    import requests
    appid = app_key
    secretKey = app_secret
    myurl = '/api/trans/vip/translate'
    fromLang = source
    toLang = target
    salt = random.randint(32768, 65536)
    q= text
    sign = app_key + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign
    try:
        response = requests.request("GET", 'https://api.fanyi.baidu.com'+myurl , data=None, headers=None, proxies=proxies)
        result = json.loads(response.text)["trans_result"]
        src = result[0]['src']
        dst = result[0]['dst']
        return dst
    except Exception as e:
        print(response.status_code)
        print(response.text)
        msg = traceback.format_exc()
        print(msg)
        return None


# ret = tranlate_single('appid','secretKey','auto','jp',{'http':'http://localhost:10809'},'How are you')
# print(ret)