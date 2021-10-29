from typing import Union
import requests, json
from typing import Union

class Translator:
    def __init__(self, apiKey: str, langCodeDB: str) -> None:
        self._key = apiKey
        self._lang_db = langCodeDB

        self.payload = {
            "key1": "value",
            "key2": "value"
        }
        self.headers = {
            'content-type': "application/json",
            'x-rapidapi-host': "webit-translator.p.rapidapi.com",
            'x-rapidapi-key': self._key
            }


    # Detect matching languages from input text in format of language code, return language with highest confidence
    def detect_lang(self, text: str) -> str:
        url = "https://webit-translator.p.rapidapi.com/detect"
        
        querystring = {"text":{text}}
        
        response = requests.request("POST", url, data=self.payload, headers=self.headers, params=querystring)
        response_text = json.loads(response.text.encode('utf8'))

        list_of_langs: list[str] = []
        detected_lang: str = ''
        # if word doesn't exist in any of the languages(typo), return 'No matches'
        try:
            for data in response_text['data']['languages']:
                for key, value in data.items():
                    if key == 'language':
                        list_of_langs.append(value)
            with open(self._lang_db, 'r') as f:
                lang_data = json.load(f)
                for lang_info in lang_data:
                    for code, language in lang_info.items():
                        if code == list_of_langs[0]:
                            detected_lang = language
        except IndexError:
            detected_lang = 'No matches'
        return detected_lang

    def translate_text(self, text: str, language: str) -> str:
        url = "https://webit-translator.p.rapidapi.com/translate"

        querystring = {"text": text,"to": language}
        

        response = requests.request("POST", url, data=self.payload, headers=self.headers, params=querystring)
        response_text = json.loads(response.text.encode('utf8'))

        translation: str = ''
        try:
            if response_text['status'] == 'success':
                for key, value in response_text['data'].items():
                    if key == 'translation':
                        translation = value
            else:
                translation = 'No translation'
        except KeyError:
            translation = 'Error'
        return translation

    # create and return list of languages from database
    def get_lst_of_langs(self) -> list[str]:
        languages: list[str] = []
        with open(self._lang_db, 'r') as f:
            lang_data = json.load(f)
            for lang_info in lang_data:
                for code, language in lang_info.items():
                    languages.append(language)
        return languages

    # get code for language from languages in database: wrong input impossible
    def get_lang_code(self, language: str) -> Union[None, str]:
        with open(self._lang_db, 'r') as f:
            lang_data = json.load(f)
            for lang_info in lang_data:
                for code, lang in lang_info.items():
                    if lang == language:
                        return code

