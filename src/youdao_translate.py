# -*- coding: utf-8 -*-
import concurrent.futures
import os
import sys
import traceback
import uuid
import requests
import hashlib
import time
from importlib import reload
import json

from my_log import log_print
from string_tool import split_strings

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/v2/api'

errorCodeMap = {
    '101': 'Required parameters are missing. First ensure that the required parameters are complete, and then confirm whether the parameters are written correctly.',
    '102': 'Unsupported language type',
    '103': 'Translated text is too long',
    '104': 'Unsupported API type',
    '105': 'Unsupported signature type',
    '106': 'Unsupported response type',
    '107': 'Unsupported transport encryption type',
    '108': 'The application ID is invalid. Register an account, log in to the backend to create an application and instance and complete the binding. You can obtain information such as application ID and application key.',
    '109': 'batchLog format is incorrect',
    '110': 'There is no valid instance of the related service, and the application has no bound service. You can create a new service and bind the service. Note: The pronunciation of the translation results of some services requires the TTS service, which can only be used after creating a speech synthesis instance in the console and binding the application.',
    '111': 'Developer account is invalid',
    '112': 'Invalid service request',
    '113': 'q cannot be empty',
    '118': 'detectLevel value error',
    '201': 'Decryption failed, possibly due to DES, BASE64, or URLDecode errors.',
    '202': 'Signature verification fails. If the correctness of the application ID and application key is confirmed and 202 is still returned, it is usually an encoding problem. Please ensure that the translated text q is UTF-8 encoded.',
    '203': 'The accessed IP address is not in the accessible IP list',
    '205': 'The requested interface is inconsistent with the application platform type. Make sure that the access method (Android SDK, IOS SDK, API) is consistent with the created application platform type. If you have any questions, please refer to the Getting Started Guide',
    '206': 'Signature verification failed due to invalid timestamp',
    '207': 'replay request',
    '301': 'Dictionary query failed',
    '302': 'Translation query failed',
    '303': 'Other exceptions on the server side',
    '304': 'Translation failed, please contact technical classmates',
    '401': 'The account is in arrears, please recharge the account',
    '402': 'offlinesdk is not available',
    '411': 'Access frequency is limited, please visit later',
    '412': 'Long requests are too frequent, please visit later'}


class TranslateResponse:
    def __init__(self, res):
        self.query = res['query']
        self.type = res['type']
        self.translatedText = res['translation']


class YoudaoTranslate(object):
    def __init__(self, app_key, app_secret, proxies=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.proxies = proxies

    def translate(self, q, source='auto', target='zh-CHS'):
        result_arrays = split_strings(q, 4800)
        ret_l = []
        cnt = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            to_do = []
            for idx, result_array in enumerate(result_arrays):
                # print(result_array)
                # l = self.translate_limit(result_array,source,target)
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

    def translate_limit(self, q, id, source='auto', target='zh-CHS'):
        try:
            qArray = q
            data = {}
            data['from'] = source
            data['to'] = target
            data['signType'] = 'v3'
            curtime = str(int(time.time()))
            data['curtime'] = curtime
            self.salt = str(uuid.uuid1())
            signStr = self.app_key + self.truncate(''.join(qArray)) + self.salt + curtime + self.app_secret
            sign = self.encrypt(signStr)
            data['appKey'] = self.app_key
            data['q'] = qArray
            data['salt'] = self.salt
            data['sign'] = sign
            # data['vocabId'] = "您的用户词表ID"
            response = self.do_request(data, self.proxies)
            contentType = response.headers['Content-Type']
            # print(contentType)
            # print(response.content)
            content = json.loads(response.content)
            # print(content['translateResults'])
            # print(content['errorCode'])
            dic = dict()
            l = []
            if content['errorCode'] == '0':
                for i in content['translateResults']:
                    translateResponse = TranslateResponse(i)
                    l.append(translateResponse)
            else:
                raise Exception('translate errorCode:' + str(content['errorCode']) + ' ' + errorCodeMap[
                    content['errorCode']] + '\nerror Result:' + str(content))
            dic['l'] = l
            dic['id'] = id
            return dic
        except Exception as e:
            msg = traceback.format_exc()
            log_print(msg)
            if os.path.isfile('translating'):
                os.remove('translating')

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data, proxies=None):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(YOUDAO_URL, data=data, headers=headers, proxies=proxies)