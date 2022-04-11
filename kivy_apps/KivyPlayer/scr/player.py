from kivy.config import Config
Config.set('graphics', 'resizable', False)
from typing import Any
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from scr.kivyScreenSize import get_screen_size
from kivymd.uix.list import OneLineListItem
from kivymd.uix.filemanager import MDFileManager
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import random
import os
import pathlib

class KivyPlayer(RelativeLayout):
    def __init__(self, **kwargs: Any) -> None:
        super(KivyPlayer, self).__init__(**kwargs)
        
        self.is_playing = False
        self.screen_size: tuple[int, int] | None = get_screen_size(appsize=False)
        if self.screen_size != None:
            Window.size = (700, 400)
        
        self.manager_open = False
        self.audio_ext = ['.mp3', '.wav']
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            ext=self.audio_ext)
        
        self.directory = ''
        self.playlist_index = 0
        self.playlist = []
        # self.playing_position = time of currently playing song.
        # will enable to resume playing song from this position.
        self.playing_position = 0
        self.loop_audio = False
        self.shuffle_audio = False

    def start_new_audio(self) -> None:
        self.ids.progress_bar.value = 0
        self.sound = SoundLoader.load(self.playlist[self.playlist_index])
        self.ids.audio_length_label.text = self.get_audio_length()
        self.ids.title_label.text = pathlib.Path(self.playlist[self.playlist_index]).stem
        self.sound.play()
        self.is_playing = True
    
    def play_pause(self) -> None:
        try:
            if self.is_playing:
                self.is_playing = False
                self.ids.play_btn.background_normal = './res/icons/pause.png'
                self.ids.play_btn.background_down = './res/icons/play.png'
                self.playing_position = self.sound.get_pos()
                self.sound.stop()
            else:
                self.is_playing = True
                self.ids.play_btn.background_normal = './res/icons/play.png'
                self.ids.play_btn.background_down = './res/icons/pause.png'
                # resume playing from last position
                if self.playing_position != 0:
                    self.sound.play()
                    self.sound.seek(self.playing_position)
                else:
                    self.start_new_audio()
        except:
            # If playlist is empty nothing will happen.
            pass
        
    def change_audio(self, option: str) -> None:
        try:
            self.sound.stop()
            self.sound.unload()
            match option:
                case 'next':
                    self.playlist_index += 1
                case 'prev':
                    self.playlist_index -= 1
                case _:
                    pass
            if self.playlist_index >= len(self.playlist):
                self.playlist_index = 0
            elif self.playlist_index < 0:
                self.playlist_index = len(self.playlist) - 1
            if self.is_playing:
                self.start_new_audio()
        except:
            pass
    
    def settings(self) -> None:
        pass
    
    def loop(self) -> None:
        # turn off shuffle
        if self.shuffle_audio:
            self.shuffle()
        if self.loop_audio:
            self.loop_audio = False
            self.ids.loop_btn.background_normal = './res/icons/loop.png'
            self.ids.loop_btn.background_down = './res/icons/repeat.png'
        else:
            self.loop_audio = True
            self.ids.loop_btn.background_normal = './res/icons/repeat.png'
            self.ids.loop_btn.background_down = './res/icons/loop.png'
    
    def shuffle(self) -> None:
        # turn off looping
        if self.loop_audio:
            self.loop()
        if self.shuffle_audio:
            self.shuffle_audio = False
            self.ids.shuffle_btn.background_normal = './res/icons/shuffle.png'
            self.ids.shuffle_btn.background_down = './res/icons/shuffle_down.png'
        else:
            self.shuffle_audio = True
            self.ids.shuffle_btn.background_normal = './res/icons/shuffle_down.png'
            self.ids.shuffle_btn.background_down = './res/icons/shuffle.png'
    
    def on_slider_move(self) -> None:
        try:
            self.playing_position = self.ids.progress_bar.value
            self.sound.seek(self.playing_position)
        except:
            pass
        
    def on_click_playlist(self, list_item: Any) -> None:
        item = list_item.text.replace('[size=11]', '').replace('[/size]', '')
        self.is_playing = True
        for i in self.playlist:
            if item == pathlib.Path(i).stem:
                try:
                    if self.sound:
                        self.sound.stop()
                        self.sound.unload()
                    self.playing_position = 0
                    self.playlist_index = self.playlist.index(i)
                    self.start_new_audio()
                except:
                    pass
    
    def update_audio_pos(self, *args: Any) -> None:
        try:
            if self.sound:
                time_sec = self.sound.get_pos()
                self.ids.audio_pos_label.text = self.convert_time(time_sec=time_sec)
                self.ids.progress_bar.max = round(self.sound.length)
                self.ids.progress_bar.value = round(time_sec)
                if self.sound.state == 'stop':
                    if self.shuffle_audio:
                        self.playlist_index = random.randint(0, len(self.playlist) - 1)
                        self.start_new_audio()
                    elif self.loop_audio:
                        self.playing_position = 0
                        # double call to play again
                        # first call will turn self.is_playing to False
                        self.play_pause()
                        self.play_pause()
                    else:
                        self.change_audio('next')
        except:
            self.ids.audio_pos_label.text = '00:00'
    
    def get_audio_length(self) -> str:
        if self.sound:
            time_sec = self.sound.length
            return self.convert_time(time_sec=time_sec)
        return '00:00'
    
    def convert_time(self, time_sec: float) -> str:
        """Return time in format '00:00' from seconds."""
        time_min = int(time_sec // 60)
        hours = int(time_min // 60)
        minutes = int(time_min % 60)
        sec = int(time_sec % 60)
        sec = round(sec)
        if len(str(sec)) == 1:
            sec = f'0{sec}'
        if len(str(minutes)) == 1:
            minutes = f'0{minutes}'
        if hours == 0:
            return f'{minutes}:{sec}'
        return f'{hours}:{minutes}:{sec}'
    
    def add_to_playlist(self) -> None:
        for i in self.playlist:
            name = pathlib.Path(i).stem
            self.ids.playlist.add_widget(OneLineListItem(text=f'[size=11]{name}[/size]',
                                                         divider='Inset',
                                                         on_release=self.on_click_playlist
                                                        ))
        if len(self.playlist) > 0:
            self.playlist_index = 0
            self.start_new_audio()

    # KivyMD File Manager  
    def file_manager_open(self) -> None:
        self.manager_open = True
        self.file_manager.show('/')

    def select_path(self, path: str) -> None:
        self.directory = path
        if os.path.isdir(self.directory):
            self.playlist = []
            self.ids.playlist.clear_widgets()
            for i in os.listdir(self.directory):
                if pathlib.Path(i).suffix in self.audio_ext:
                    self.playlist.append(f'{self.directory}/{i}')
        else:
            self.playlist.append(self.directory)
        self.exit_manager()
        
    def exit_manager(self, *args: Any) -> None:
        self.manger_open = False
        self.file_manager.close()
        self.add_to_playlist()
        print(self.directory)
       
class Application(MDApp):
    title = 'KivyPlayer'
    icon = './res/icon.png'
    Window.clearcolor = (68/255.0, 122/255.0, 156/255.0, 0.8)
    
    def build(self) -> RelativeLayout:
        _app = KivyPlayer()
        Clock.schedule_interval(_app.update_audio_pos, 1)
        return _app
