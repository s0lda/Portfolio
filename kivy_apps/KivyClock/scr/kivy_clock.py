from typing import Any
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivymd.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
from kivy.clock import Clock
from scr.screen_size import get_screen_size
from datetime import datetime

# stopwatch is a timer and timer is a stopwatch
# as I thought that's how they were meant to be called
# but it is the other way round
# only changed name of the tab so it displays correctly in the app.

class KivyClock(TabbedPanel):
    _time = datetime.now().strftime('%H:%M:%S')
    is_timer_running = False
    timer_time = 0
    is_stopwatch_running = False
    stop_watch_time = 0
    
    def set_stopwatch(self, run: bool=False, 
                      stop: bool=False, 
                      up: int=0, down: int=0) -> None:
        
        self.stop_watch_time += up
        self.stop_watch_time -= down
        
        if self.stop_watch_time < 0:
            self.stop_watch_time = 0
        
        if run:
            if not stop:
                if self.is_stopwatch_running:
                    self.is_stopwatch_running = False
                    self.ids.stopwatch_btn.background_color: (36/255, 121/255, 158/255, 1)
                    self.ids.stopwatch_btn.background_down: (36/255, 121/255, 158/255, 1)
                    self.ids.stopwatch_btn.text = 'Start'
                else:
                    self.is_stopwatch_running = True
                    self.ids.stopwatch_btn.text = 'Pause'
            else:
                self.is_stopwatch_running = False
                self.stop_watch_time = 0
                self.ids.stopwatch_lbl.text = self.convert_time(self.stop_watch_time)
                self.ids.stopwatch_btn.text = 'Start'
    
    def set_timer(self, stop: bool=False) -> None:
        if not stop:
            if self.is_timer_running:
                self.is_timer_running = False
                self.ids.timer_btn.background_color: (36/255, 121/255, 158/255, 1)
                self.ids.timer_btn.background_down: (36/255, 121/255, 158/255, 1)
                self.ids.timer_btn.text = 'Start'
            else:
                self.is_timer_running = True
                self.ids.timer_btn.text = 'Pause'
        else:
            self.is_timer_running = False
            self.timer_time = 0
            self.ids.timer_lbl.text = self.convert_time(self.timer_time)
            self.ids.timer_btn.text = 'Start'
    
    def callback(self, *args: Any) -> None:
        self._time = datetime.now().strftime('%H:%M:%S')
        self.ids.time_lbl.text = self._time
        
        if self.is_timer_running:
            self.timer_time += 1
            self.ids.timer_lbl.text = self.convert_time(self.timer_time)
            self.ids.timer_btn.text = 'Pause'
        else:
            self.ids.timer_btn.text = 'Start'
        
        if self.timer_time != 0:
            self.ids.timer_btn_stop.disabled = False
        else:
            self.ids.timer_btn_stop.disabled = True
            
        self.ids.stopwatch_lbl.text = self.convert_time(self.stop_watch_time)
        
        if self.stop_watch_time != 0:
            self.ids.stopwatch_btn_stop.disabled = False
            self.ids.stopwatch_btn.disabled = False
        else:
            self.ids.stopwatch_btn.disabled = True
            self.ids.stopwatch_btn_stop.disabled = True
            
        if self.is_stopwatch_running:
            self.stop_watch_time -= 1
            if self.stop_watch_time == 0:
                self.is_stopwatch_running = False

        
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
            hours = '00'
        return f'{hours}:{minutes}:{sec}'
        
class Application(App):
    title = 'Kivy Clock'
    icon = './res/icon.png'
    screen_size = get_screen_size()
    if screen_size != None:
        Window.size = (400, 600)
    Window.clearcolor = (230/255, 230/255, 230/255, 1)
    
    def build(self):
        _app = KivyClock()
        Clock.schedule_interval(_app.callback, 1)
        return _app
