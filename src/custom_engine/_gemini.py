import threading
import json
import os
import io
import time
import concurrent.futures
import traceback
import requests

limit_time_span_dic = dict()
lock = threading.Lock()
count = 0
api_key = ""
rpm = 0
rps = 0
tpm = 0
model = ""
base_url = ""
proxies = None
time_out = 0
max_length = 0
gemini_template_file = 'openai_template.json'


def translate_queue(app_key, app_secret, source, target, proxies, q):
    # write import inside the function , otherwise will cause NameError

    global gemini_template_file
    def translate_gemini_batch(api_key_to_use, source_lang, target_lang, proxy_settings, text_list):

        global model, time_out
        if not model:
            model = 'gemini-2.0-flash'
        if not time_out or time_out <= 0:
            time_out = 120 

        gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key_to_use}"

        ori_dic = {str(i): text for i, text in enumerate(text_list)}
        json_to_translate = json.dumps(ori_dic, ensure_ascii=False)

        messages = []
        try:
            with io.open(gemini_template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
                template_content = template_content.replace('#SOURCE_LANGUAGE_ID!@$^#', source)
                template_content = template_content.replace('#TARGET_LANGAUGE_ID!@$^#', target)
                messages = json.loads(template_content)
        except Exception as e:
            print(f"Error reading or parsing {gemini_template_file}: {e}")
            return None

        if not messages:
            print(f'{gemini_template_file} is not a valid json template or is empty.')
            return None
        full_prompt_text = ""
        for message in messages:
            full_prompt_text += message.get("content", "") + "\n"
        
        full_prompt_text = full_prompt_text.replace('#JSON_DATA_WAITING_FOR_TRANSLATE_ID!@$^#', json_to_translate)
        
        payload = {
            "contents": [
                {
                    "role": "user", 
                    "parts": [
                        {
                            "text": full_prompt_text 
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.5, 
                "topP": 1,
                "topK": 1,
                "maxOutputTokens": 8192,
                "response_mime_type": "application/json" 
            }
        }

        try:
            response = requests.post(
                gemini_api_url,
                json=payload,
                proxies=proxy_settings,
                timeout=time_out
            )
            response.raise_for_status()

            response_json = response.json()
            content_text = response_json['candidates'][0]['content']['parts'][0]['text']
            translated_dic = json.loads(content_text)

            if len(translated_dic) != len(ori_dic):
                print("Warning: Mismatch between original and translated item count.")
            
            l = []
            for key, translated_text in translated_dic.items():
                if key in ori_dic:
                    item = {
                        'untranslatedText': ori_dic[key],
                        'translatedText': translated_text
                    }
                    l.append(item)

            return l

        except Exception:
            if 'response' in locals():
                print(response.status_code)
                print(response.text)
            msg = traceback.format_exc()
            print(msg)
            return []

    api_key_to_use = app_key if app_key else api_key
    if not api_key_to_use:
        print("Gemini API key is missing.")
        return []

    return translate_gemini_batch(api_key_to_use, source, target, proxies, q)