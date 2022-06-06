from typing import Any

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from KivyOnTop import register_topmost

from scr.screen_size import get_screen_size
from scr.scanner import PCScanner

class SplashScreen(Screen):
    '''
    Set on enter activities.
    Display app logo for 5 seconds.
    '''
    
    def on_enter(self, *args: Any) -> None:
        '''
        Schedule the switch to main screen.
        '''
        Clock.schedule_once(self.switch_to_main, 5)
    
    def switch_to_main(self, dt: float) -> None:
        self.manager.current = 'main_screen'


class MainScreen(Screen):
    pc = PCScanner()
    cpu_name = pc.get_cpu_name().split('CPU')[0]
    total_ram = pc.get_total_ram()
    ram = f'{total_ram} GB'
    gpu_name = pc.get_gpu_name()
    total_storage = f'{pc.get_storage_data()[0]} GB'
    
    def on_enter(self, *args: Any) -> None:
        Clock.schedule_interval(self.update_cpu_usage, 1)
        Clock.schedule_interval(self.update_ram_usage, 1)
        Clock.schedule_interval(self.update_gpu_temp, 1)
        Clock.schedule_interval(self.update_gpu_load, 1)
        Clock.schedule_interval(self.update_storage_usage, 1)
    
    def update_cpu_usage(self, dt: float) -> None:
        self.ids.cpu_usage.value = self.pc.get_cpu_load()
        
    def update_ram_usage(self, dt: float) -> None:
        self.ids.ram_usage.value = self.pc.get_ram_usage()
        
    def update_gpu_temp(self, dt: float) -> None:
        self.ids.gpu_temp.text = f'{self.pc.get_gpu_temp()} °C'
        
    def update_gpu_load(self, dt: float) -> None:
        # print(self.pc.get_gpu_load())
        self.ids.gpu_load.value = self.pc.get_gpu_load()
        
    def update_storage_usage(self, dt: float) -> None:
        self.ids.storage_usage.max = self.pc.get_storage_data()[0]
        self.ids.storage_usage.value = self.pc.get_storage_data()[1]
        
class ScreenManager(ScreenManager):
    pass

class PerformanceMonitor(App):
    title = 'Performance Monitor'
    icon = '.res/icon.png'
    
    def set_window_properties(self) -> None:
        screen_size = get_screen_size()
        if screen_size != None:
            window_app_width, window_app_height = 200, 400
            
            Window.size = (window_app_width, window_app_height)
            Window.borderless = True
            
            # set Window position to right top corner of the screen
            Window.top = 0.0
            Window.left = screen_size[0] - window_app_width
            
            # keep widget always on top of other Windows
            register_topmost(Window, self.title)
        
    def build(self) -> Widget | None:
        self.set_window_properties()
        return super().build()
