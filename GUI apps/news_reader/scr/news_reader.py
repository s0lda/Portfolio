import json
from urllib.request import urlopen
from datetime import datetime

class NewsReader():
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.location = self.get_location()

    def read_news(self, search: str | None) -> list[list[str]]:
        if search != None:
            date_now = datetime.now()
            today = datetime.strftime(date_now, '%Y-%m-%d')
            search = f'everything?q={search}&from={today}&sortBy=popularity&'
            print(search)
            print(today)
        else:
            search = f'top-headlines?country={self.location}&'
        response = urlopen(f'https://newsapi.org/v2/{search}'
                    f'pageSize=100&'
                    f'apiKey={self.api_key}')
        data = json.load(response)
        news: list[list[str]] = []
        for article in data['articles']:
            news.append([article['title'], article['url']])
        for item in news:
            print(item)
        return news

    def get_location(self) -> str:
        """
        It will return country location in format: gb, us etc.
        """

        response = urlopen('http://ipinfo.io/json')
        data = json.load(response)
        return data['country'].lower()
