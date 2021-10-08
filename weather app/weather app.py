import tkinter as tk
import requests, json, os
from tkinter import StringVar, ttk
from pathlib import Path


class Window(tk.Tk):
    def __init__(self, database: object, icons: str) -> None:
        super().__init__()
        self._db = database
        self._icons = icons
 
        self.enter_city()
        self.update_vars()
        self.labels()
        self.weather_img()
        # auto update function, 'while typing' style    
        self.update_data()
        
        self.geometry('350x450')
        self.title('Weather App')
        self.iconbitmap(f'{icons}\\icon.ico')


    def weather_img(self) -> None:
        # set weather image
        self.icon = StringVar()
        self.icon.set(WeatherData.get_icon_code(self.weather))
        # weather icon path
        weather_icon = Path(f'{icons}\\{self.icon.get()}.png')
        # ensure during changing city when icon code not availabe there is no error, refresh icon on the screen
        if weather_icon.is_file():
            self.weather_image = tk.PhotoImage(file=f'{icons}\\{self.icon.get()}.png')
        else:
            self.weather_image = tk.PhotoImage(file=f'{icons}\\refresh.png')
        self.image_lbl = ttk.Label(self, image=self.weather_image)
        self.image_lbl.place(x=45, y=35)            


    def enter_city(self) -> None:
        # City entry
        self.city_ent = ttk.Entry(self, justify='center', width=50)
        self.city_ent.place(x=20, y=10)
        self.city_var = StringVar(value='Warsaw')


    def update_vars(self) -> None:
        # Get weather data for City
        self.weather = WeatherData.get_weather(self._db, self.city_var.get())
        
        # set vars for auto update
        self.temp = StringVar()
        self.temp.set(WeatherData.get_temp(self.weather))
        self.wind = StringVar()
        self.wind.set(WeatherData.get_wind_direction(self.weather))
        self.prediction = StringVar()
        self.prediction.set(WeatherData.get_predicted_weather(self.weather))


    def labels(self) -> None:
        self.city_lbl = ttk.Label(self, textvariable=self.city_var, width=35, font=('Helvetica', 12, 'bold'), anchor='center')
        self.city_lbl.place(x=10, y=290)
        self.city_ent.configure(textvariable=self.city_var)

        self.temp_lbl = ttk.Label(self, text='Temperature:', font=('Helvetica', 11))
        self.temp_lbl.place(x=10, y=330)

        self.wind_lbl = ttk.Label(self, text='Wind direction:', font=('Helvetica', 11))
        self.wind_lbl.place(x=10, y=360)

        self.prediction_lbl = ttk.Label(self, text='Predicted weather:', font=('Helvetica', 11))
        self.prediction_lbl.place(x=10, y=390)

        self.temp_val_lbl = ttk.Label(self, textvariable=self.temp, font=('Helvetica', 11))
        self.temp_val_lbl.place(x=220, y=330)
        
        self.wind_val_lbl = ttk.Label(self, textvariable=self.wind, font=('Helvetica', 11))
        self.wind_val_lbl.place(x=220, y=360)

        self.prediction_val_lbl = ttk.Label(self, textvariable=self.prediction, font=('Helvetica', 11))
        self.prediction_val_lbl.place(x=220, y=390)
        
        
    def update_data(self) -> None:
        self.weather = WeatherData.get_weather(self._db, self.city_var.get())
        self.temp.set(WeatherData.get_temp(self.weather))
        self.wind.set(WeatherData.get_wind_direction(self.weather))
        self.prediction.set(WeatherData.get_predicted_weather(self.weather))
        # destroy icon label, so new one won't be on top of old one
        self.image_lbl.destroy()
        # refresh icon label
        self.weather_img()
        self.after(1000, self.update_data)



class WeatherData:
    def __init__(self, key: str) -> None:
        self._key = key

    # excepting KeyError for autoupdate. App won't stop working while typing new city name

    def get_weather(self, city: str) -> list:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self._key}'
        response = requests.get(url)
        data = response.json()
        return data


    def get_temp(data: list) -> str:
        try:
            celsius = data['main']['temp']
            return str(round(celsius))
        except KeyError:
            pass


    def get_predicted_weather(data: list) -> str:
        try:    
            sky = data['weather']
            for item in sky:
                for key, value in item.items():
                    if key == 'main':
                        return str(value)
        except KeyError:
            pass


    def get_wind_direction(data: list) -> str:
        try:    
            wind = data['wind']['deg']
            if wind == 0:
                return 'North'
            elif wind > 0 and wind < 90:
                return 'North East'
            elif wind == 90:
                return 'East'
            elif wind > 90 and wind < 180:
                return 'South East'
            elif wind == 180:
                return 'South'
            elif wind > 180 and wind < 270:
                return 'South West'
            elif wind == 270:
                return 'West'
            else:
                return 'North West'
        except KeyError:
            pass


    # get icon code to display right weather icon
    def get_icon_code(data: list) -> str:
        try:    
            info = data['weather']
            for item in info:
                for key, value in item.items():
                    if key == 'icon':
                        return value
        except KeyError:
            pass


if __name__ == "__main__":
    _current_path = os.path.dirname(__file__)
    
    # Free API key
    with open(f'{_current_path}\\settings\\apiconfig.json', 'r') as f:
        api_file = json.load(f)
        for key, value in api_file.items():
            if key == 'key':
                _api_key = value
    
    # icons folder
    icons = f'{_current_path}\\icons'
    
    db = WeatherData(_api_key)
    Window(db, icons).mainloop()
