from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from scr.kivyScreenSize import get_screen_size
from scr.ytdownloader import Downloader
from pathlib import Path

class YTD(RelativeLayout):
    _d_path = str(Path.home() / 'Downloads')
    downloader = Downloader(download_path=_d_path)

    def download(self, is_mp3: bool, is_mp4: bool, url: str) -> None:
        if is_mp3 == False and is_mp4 == False:
            self.ids.msg_lbl.text = 'Choose what type of file you want to download.'
        else:
            resp = self.downloader.download(is_mp3=is_mp3, is_mp4=is_mp4, url=url)
            self.ids.url_input.text = ''
            self.ids.msg_lbl.text = resp[0]

class YouTubeDownloader(App):
    def build(self) -> RelativeLayout:
        screen_size: tuple[int, int] | None = get_screen_size(appsize=False)
        if screen_size != None:
            Window.size = (850, 400)
        self.title = 'YouTube Downloader'
        self.icon = './res/icon.png'
        return YTD()
