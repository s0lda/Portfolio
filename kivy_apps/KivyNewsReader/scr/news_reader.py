import json
from urllib.request import urlopen
from datetime import datetime
import sys

class NewsReader():
    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key
        # Close application if API key is not found.
        if self.api_key == None:
            sys.exit()
        self.location = self.get_location()

    def read_news(self, search: str | None) -> list[list[str]]:
        """
        Read news from newsapi.org.
        Return list of news [title, article url, image url.].
        """
        if search != None:
            date_now = datetime.now()
            today = datetime.strftime(date_now, '%Y-%m-%d')
            search = f'everything?q={search}&from={today}&sortBy=popularity&'
        else:
            search = f'top-headlines?country={self.location}&'
        response = urlopen(f'https://newsapi.org/v2/{search}'
                    f'pageSize=100&'
                    f'apiKey={self.api_key}')
        data = json.load(response)
        news: list[list[str]] = []
        for article in data['articles']:
            news.append([article['title'], article['url'], article['urlToImage']])
        return news

    def get_location(self) -> str:
        """
        It will return country location in format: gb, us etc.
        """

        response = urlopen('http://ipinfo.io/json')
        data = json.load(response)
        return data['country'].lower()
