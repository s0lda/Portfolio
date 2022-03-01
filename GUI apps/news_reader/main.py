from scr.app import App
from scr.news_reader import NewsReader
from scr.error import ErrorWin
from scr.screen_size import get_screen_size
import os, sys
from dotenv import load_dotenv

def get_api_key() -> str | None:
    try:
        _file = f'{os.path.dirname(__file__)}//scr//init.env'
        load_dotenv(_file)
        return os.getenv('News-API')
    except:
        return None

def main() -> None:
    _screen_size = get_screen_size()
    _res = f"{os.path.dirname(__file__)}//res"
    _api_key = get_api_key()

    if _screen_size != None:    
        if _api_key != None:
            App(res_dir=_res, 
                reader=NewsReader(api_key=_api_key),
                scree_size=_screen_size).mainloop()
        else:
            ErrorWin(res_dir=_res,
                screen_size=_screen_size,
                error_type="ERROR: Couldn't find API KEY.").mainloop()
    else:
        sys.exit()

if __name__ == '__main__':
    main()
