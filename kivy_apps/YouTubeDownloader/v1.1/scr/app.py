from typing import Any

from kivy.config import Config
Config.set('graphics', 'resizable', False)

from multiprocessing.pool import ThreadPool
from pathlib import Path
from datetime import datetime

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from scr.screen_size import get_screen_size
from scr.ytdownloader import Downloader


class SplashScreen(Screen):
    '''
    Splash Screen Class. Does nothing apart of displaying app logo.
    '''
    def on_enter(self, *args: Any) -> None:
        '''Set on enter activities.'''
        Clock.schedule_once(self.switch_to_download, 4)
    
    def switch_to_download(self, dt: float) -> None:
        '''Switch to download screen.'''
        self.manager.current = 'download_screen'

class FileManager(Screen):
    pass

class InfoScreen(Screen):
    pass

class HistoryScreen(Screen):
    def load_table(self) -> None:
        '''Loads the table.'''
        # layout = AnchorLayout()
        self.table = MDDataTable(
            size_hint=(0.96, 0.82),
            pos_hint={'x': 0.02, 'y': 0.15},
            use_pagination=True,
            check=False,
            column_data=[
                ('Name', dp(59)),
                ('Time', dp(20)),
                ('Date', dp(20)),
            ],
            row_data=[
                (
                    f'{i[0]}',
                    f'{i[1]}',
                    f'{i[2]}',
                )
                for i in YouTubeDownloader().get_download_history()
            ]
        )
        self.add_widget(self.table)
        
    def on_enter(self, *args: Any) -> None:
        self.load_table()

class DownloadScreen(Screen):
    d_path = str(Path.home() / 'Downloads')
    progress_value = 0
    _downloader = Downloader(d_path)
    
    def on_download(self, is_mp3: bool, is_mp4: bool, url: str) -> None:
        if is_mp3 == False and is_mp4 == False:
            self.ids.info_lbl.text = 'Please select a type of file to download.'
        else:
            self.ids.info_lbl.text = 'Downloading...'
            
            self.is_mp3 = is_mp3
            self.is_mp4 = is_mp4
            self.url = url
            
            Clock.schedule_once(self.schedule_download, 2)
            Clock.schedule_interval(self.start_progress_bar, 0.1)
            
    def schedule_download(self, dt: float) -> None:
        '''
        Callback method for the download.
        '''
        
        pool = ThreadPool(processes=1)
        _downloader = Downloader(self.d_path)
        self._downloader = _downloader
        self.async_result = pool.apply_async(_downloader.download,
                                             (self.is_mp3, self.is_mp4, self.url))
        Clock.schedule_interval(self.check_process, 0.1)
        
    def check_process(self, dt: float) -> None:
        '''
        Check if download is complete.
        '''
        if self.async_result.ready():
            resp = self.async_result.get()
            
            if resp[0] == 'Error. Download failed.':
                self.ids.info_lbl.text = resp[0]
                # progress bar gray if error
                self.stop_progress_bar(value=0)
            else:
                # progress bar blue if success
                self.stop_progress_bar(value=100)
                self.ids.file_name.text = resp[0]
                self.ids.info_lbl.text = 'Finished downloading.'
                self.ids.url_input.text = ''
                
                time = datetime.now()
                date = time.strftime("%d/%m/%Y")
                time = time.strftime("%H:%M:%S")
                YouTubeDownloader().add_to_history(resp[0], time, date)
            
            Clock.unschedule(self.check_process)
           
    def update_path_lbl(self) -> None:
        self.ids.download_path.text = self.d_path
        
    def start_progress_bar(self, dt: float) -> None:
        '''
        Callback method for progress bar.
        '''
        # self.progress_value += 1
        # if self.progress_value >= 100:
        #     self.progress_value = 0
        self.ids.progress_bar.max = self._downloader.get_file_size()
        self.progress_value = self._downloader.get_bytes_received()
        self.ids.progress_bar.value = self.progress_value
    
    def stop_progress_bar(self, value: int) -> None:
        '''
        Will stop progress bar schedule and progress bar will stop
        at desired value. 0 for error and 100 for success.
        '''
        self.ids.progress_bar.value = value
        Clock.unschedule(self.start_progress_bar)
        self.progress_value = 0

class YouTubeDownloader(MDApp):
    title = 'Youtube Downloader'
    icon = './res/icon.png'
    history: list[tuple[str, str, str]] = []
    
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
        '''
        Changes the download path across the application.
        Will update d_path in DownloadScreen.
        '''
        self.current_path = path
        dowload_screen = self.get_screen_instance('download_screen')
        dowload_screen.d_path = self.current_path # type: ignore
        dowload_screen.update_path_lbl()          # type: ignore
        
    def get_screen_instance(self, screen_name: str) -> Screen:
        '''Return instance of Screen class.'''
        return MDApp.get_running_app().root.get_screen(screen_name) # type: ignore
    
    def add_to_history(self, name: str, time: str, date: str) -> None:
        item = (name, time, date)
        self.history.append(item)
        
    def get_download_history(self) -> list[tuple[str, str, str]]:
        return self.history
        
    def build(self) -> ScreenManager:
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name='splash_screen'))
        self.sm.add_widget(DownloadScreen(name='download_screen'))
        self.sm.add_widget(InfoScreen(name='info_screen'))
        self.sm.add_widget(FileManager(name='file_manager'))
        self.sm.add_widget(HistoryScreen(name='history_screen'))
        return self.sm
