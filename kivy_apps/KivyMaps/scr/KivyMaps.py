from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.dropdown import DropDown
from kivy.garden.mapview import MapView, MapMarker
from scr.get_location import Location
from scr.screen_size import get_screen_size
from scr.data_manager import DataManager

class SettingsDropDown(DropDown):
    data_mng = DataManager()

    def set_home(self, lat: float, lon: float) -> None:
        '''
        Set home latitude and longitude.
        '''
        data = self.data_mng.get_settings()
        data['home'] = {'latitude': lat, 'longitude': lon}
        self.data_mng.save_settings(data)
        
    def remove_home(self) -> None:
        '''
        Remove home latitude and longitude.
        '''
        data = self.data_mng.get_settings()
        data['home'] = {'latitude': None, 'longitude': None}
        self.data_mng.save_settings(data)

class KivyMap(RelativeLayout):
    def __init__(self, lat: float, lon: float) -> None:
        super().__init__() # type: ignore
        self.lat = lat
        self.lon = lon
        self.marker = None
        self.data_mng = DataManager()
        self.dropdown = SettingsDropDown()
        self.location = Location()
        self.dist_calc = DistanceCalculator()
        self.ids.settings_button.bind(on_release=self.dropdown.open)
        self.set_start_location()

        
    def place_marker(self) -> None:
        '''
        Place marker on the map. Source for marker:
        map latitude and map longitude.
        If marker is already placed, remove it.
        '''
        if self.marker:
            self.ids.map.remove_widget(self.marker)
        self.marker = MapMarker(lat=self.ids.map.lat,
                           lon=self.ids.map.lon,
                           source='./res/icons/marker.png')
        self.ids.map.add_marker(self.marker)
 
    def set_start_location(self) -> None:
        '''
        Set start location if user current location is available.
        '''
        if self.lat != None and self.lon != None:
            self.move_to_target()
            
    def get_current_location(self) -> list[str] | None:
        location = self.location.get_usr_location()
        if location != None:
            self.lat = location[0]
            self.lon = location[1]
            self.move_to_target()
                     
    def on_search(self, address: str) -> None:
        '''
        Search for the address and set the location.
        '''
        location = Location().find_lat_lon(address=address)
        if location != None:
            self.lat = location[0]
            self.lon = location[1]
            self.move_to_target()
            
    def on_home_pressed(self) -> None:
        home = self.data_mng.get_settings()['home']
        if home['latitude'] != None and home['longitude'] != None:
            self.lat = home['latitude']
            self.lon = home['longitude']
            self.move_to_target()
            
    def move_to_target(self, init: bool=False) -> None:
        '''
        Move map to target location.
        '''
        self.ids.map.lat = self.lat
        self.ids.map.lon = self.lon
        self.ids.map.center_on(self.ids.map.lat, self.ids.map.lon)
        self.place_marker()

    
class Application(App):
    title = 'Kivy Maps'
    icon = './res/icon.png'
    location = Location().get_usr_location()
    
    # set the size of the APP window    
    _screen_size = get_screen_size()
    window_width, window_height = 1920, 1080
    is_fullscreen = False
    # if Monitor resolution is lower than APP window,
    # then set the size of the APP window to the Monitor resolution
    if _screen_size != None:
        if _screen_size[0] < window_width or _screen_size[1] < window_height:
            window_width, window_height = _screen_size[0], _screen_size[1]
            is_fullscreen = True
        Window.size = (window_width, window_height)
        if not is_fullscreen:
            Window.left = (_screen_size[0] - window_width) / 2
            Window.top = (_screen_size[1] - window_height) / 2
        else:
            Window.left = 0
            Window.top = 30
    
    def build(self) -> RelativeLayout:
        if self.location != None:
            _app = KivyMap(lat=self.location[0],
                           lon=self.location[1])
        else:
            # default location is set to London, UK
            _app = KivyMap(lat=51.509865,
                           lon=-0.118092)
        return _app
