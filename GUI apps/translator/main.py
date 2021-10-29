import os, sys
sys.path.append(f'{os.path.dirname(__file__)}\\scripts')
from typing import Any
from dotenv import load_dotenv
from scripts.window import Window
from scripts.translator import Translator

def main() -> None:
    load_dotenv(dotenv_path=f'{os.path.dirname(__file__)}\\init.env')

    _lng_db = f'{os.path.dirname(__file__)}\\lang_codes.json'
    _api_key: Any = os.getenv('X-RapidAPI-Key')
    _trs = Translator(apiKey=_api_key, langCodeDB=_lng_db)
    app = Window(translator=_trs)
    app.mainloop()


if __name__ == '__main__':
    main()
