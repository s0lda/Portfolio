from typing import Any
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
from kivy.uix.image import AsyncImage
from scr.screen_size import get_screen_size
from scr.news_reader import NewsReader
import os
import webbrowser
from dotenv import load_dotenv

def read_api_key() -> str | None:
    try:
        _file = f'./scr/init.env'
        load_dotenv(_file)
        return os.getenv('News-API')
    except:
        return None

class NewsReader(RelativeLayout):
    reader = NewsReader(api_key=read_api_key())
    news_url: dict[str, str] = {}
    
    def open_news_website(self, url: str | None) -> None:
        if url != None:
            try:
                webbrowser.open(url, new=2)
            except:
                pass
            
    def find_news_url(self, list_item: Any) -> None:
        """
        Will find news url in news_url dict.
        """
        title = list_item.text
        for key, value in self.news_url.items():
            if key == title:
                self.open_news_website(value)
    
    def update_news(self, search: str | None=None) -> None:
        """
        Will add content to a news list, standard news from current location if possible.
        It will clear the list before adding new content eg. new search.
        """
        self.news_url = {}
        self.ids.news_list.clear_widgets()
        
        news_list = self.reader.read_news(search)
        for news in news_list:
            self.news_url[news[0]] = news[1]
            # Try to get img url if that exists. Can be None Sometimes.
            try:
                img_url = news[2]
                try:
                    img_url = img_url.split('?')[0]
                    print(img_url)
                    url_image = AsyncImage(source=img_url)
                    icon = IconLeftWidget(icon=url_image)
                # In case of any errors with loading image.
                # There is a fallback image.
                except AttributeError:
                    icon = IconLeftWidget(icon='image')
            except ValueError:
                icon = IconLeftWidget(icon='image')
            news_item = OneLineAvatarListItem(
                text=news[0],
                divider='Inset',
                on_release=self.find_news_url,
                )
            
            news_item.add_widget(icon)
            self.ids.news_list.add_widget(news_item)


class Application(MDApp):
    def __init__(self, resources: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.res = resources
    
    def build(self) -> RelativeLayout:
        self.title = 'News Reader'
        self.icon = f'{self.res}icon.png'
        _app = NewsReader()
        _app.update_news()
        if get_screen_size() != None:
            Window.size = (400, 650)
        return _app
