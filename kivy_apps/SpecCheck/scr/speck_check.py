from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from scr.kivyScreenSize import get_screen_size
import GPUtil
import cpuinfo
import platform
import psutil
import getpass

class Checker(RelativeLayout):
    os = platform.system()
    os_ver = platform.release()
    user_name = getpass.getuser()
    machine_name = platform.node()
    cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    cpu_freq = psutil.cpu_freq().current
    cpu_cores = psutil.cpu_count(logical=False)
    ram = round(psutil.virtual_memory()[0] / 1024.**3, 2)
    gpu = GPUtil.getGPUs()[0]
    
    def insert_data(self) -> None:
        self.ids.os_lbl.text = self.os
        self.ids.os_ver_lbl.text = self.os_ver
        self.ids.user_lbl.text = self.user_name
        self.ids.machine_lbl.text = self.machine_name
        self.ids.cpu_lbl.text = self.cpu_name
        self.ids.cpu_freq_lbl.text = f'{self.cpu_freq} MHz'
        self.ids.cpu_cores_lbl.text = f'{self.cpu_cores}'
        self.ids.ram_lbl.text = f'{self.ram} GB'
        self.ids.gpu_lbl.text = f'{self.gpu.name}'
        self.ids.gpu_mem_lbl.text = f'{self.gpu.memoryTotal} MB'
        self.ids.gpu_uuid_lbl.text = f'{self.gpu.uuid}'
        self.ids.gpu_driver_lbl.text = f'{self.gpu.driver}'
        
class SpecCheck(App):
    def build(self) -> RelativeLayout:
        screen_size: tuple[int, int] | None = get_screen_size(appsize=False)
        if screen_size != None:
            Window.size = (450, 550)
        self.title = 'Spec Check'
        self.icon = './res/icon.png'
        _app = Checker()
        _app.insert_data()
        return _app
