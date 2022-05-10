from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from scr.screen_size import get_screen_size
from scr.ytdownloader import Downloader
from pathlib import Path


class FileManager(Screen):
    pass

class HistoryScreen(Screen):
    pass

class InfoScreen(Screen):
    pass

class DownloadScreen(Screen):
    d_path = str(Path.home() / 'Downloads')
    
    def on_download(self, is_mp3: bool, is_mp4: bool, url: str) -> None:
        if is_mp3 == False and is_mp4 == False:
            self.ids.info_lbl.text = 'Please select a type of file to download.'
        else:
            self.ids.info_lbl.text = ''
            
            _downloader = Downloader(self.d_path)
            
            resp = _downloader.download(is_mp3, is_mp4, url)
            if resp[0] == 'Error. Download failed.':
                self.ids.info_lbl.text = resp[0]
            else:    
                self.ids.file_name.text = resp[0]
            self.ids.url_input.text = ''
    
    def update_path_lbl(self) -> None:
        print(self.d_path)
        self.ids.download_path.text = self.d_path

class YouTubeDownloader(MDApp):
    title = 'Youtube Downloader'
    icon = './res/icon.png'
    
    app_width, app_height = 550, 400
    _screen_size = get_screen_size()
    if _screen_size is not None:
        if app_width > _screen_size[0] or app_height > _screen_size[1]:
            Window.size = _screen_size
        else:
            Window.size = (app_width, app_height)
    
    # set the path for file chooser
    # file_chooser will use current_path
    # every time is called to stay in choosen directory.      
    current_path = DownloadScreen().d_path
    
    def change_d_path(self, path: str) -> None:
        '''Changes the download path across the application.'''
        self.current_path = path
        dowload_screen = self.get_instance_of_download_screen()
        dowload_screen.d_path = self.current_path
        dowload_screen.update_path_lbl()
        
    def get_instance_of_download_screen(self) -> DownloadScreen:
        '''Will return current instance of DownloadScreen for updating GUI.'''
        return MDApp.get_running_app().root.get_screen('download_screen')
        
    def build(self) -> ScreenManager:
        self.sm = ScreenManager()
        self.sm.add_widget(DownloadScreen(name='download_screen'))
        self.sm.add_widget(InfoScreen(name='info_screen'))
        self.sm.add_widget(FileManager(name='file_manager'))
        return self.sm