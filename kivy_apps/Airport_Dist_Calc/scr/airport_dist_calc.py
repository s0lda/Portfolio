from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from scr.kivyScreenSize import get_screen_size
from scr.airportDistanceChecker import AirportDistanceChecker

class ADC(RelativeLayout):
    _db = AirportDistanceChecker(database='./res/airports.csv')
    
    def fill_data(self) -> None:
        departure = self._db.get_airport_details(self.ids.departure.text)
        arrival = self._db.get_airport_details(self.ids.arrival.text)
        if self.ids.departure.text != '':
            if departure != None:
                dep_location = f'{departure[0]}, {departure[5]}, {departure[4]}'
                self.ids.from_label.text = dep_location
            else:
                self.ids.from_label.text = 'Airport not found'
        if self.ids.arrival.text != '':
            if arrival != None:
                arr_location = f'{arrival[0]}, {arrival[5]}, {arrival[4]}'
                self.ids.to_label.text = arr_location
            else:
                self.ids.to_label.text = 'Airport not found'
        if departure != None and arrival != None:
            dep = departure[1], departure[2]
            arr = arrival[1], arrival[2]
            distance = self._db.get_airport_distance(dep, arr)
            self.ids.distance.text = f'Distance {distance} km'
            
            # flight time calculation
            # distance divided by average speed of the commercial plane in km/h
            time = distance / 800
            time = round(time, 2)
            time = time * 60
            hour = int(time // 60)
            minutes = int(time % 60)
            if hour == 0:
                self.ids.flight_time.text = f'Flight time {minutes} minutes'
            elif hour == 1 and minutes == 0:
                self.ids.flight_time.text = f'Flight time {hour} hour'
            elif hour == 1 and minutes != 0:
                self.ids.flight_time.text = f'Flight time {hour} hour {minutes} minutes'
            else:
                if minutes == 0:
                    self.ids.flight_time.text = f'Flight time {hour} hours'
                else:
                    self.ids.flight_time.text = f'Flight time {hour} hours {minutes} minutes'
            
            
class Application(App):
    def build(self):
        screen_size: tuple[int, int] | None = get_screen_size(appsize=False)
        if screen_size != None:
            Window.size = (400, 600)
        # background color
        Window.clearcolor = (103/255.0, 105/255.0, 111/255.0, 0.3)
        self.title = 'Airport Distance Calculator'
        self.icon = './res/icon.png'
        return ADC()
