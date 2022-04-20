import os
import json

class DataManager:
    def __init__(self) -> None:
        self.path = './data/'
        self.settings_path = f'{self.path}settings.json'
        
    def get_settings(self) -> dict[str, dict[str, float | None] | list[list[float]]]:
        if not os.path.exists(self.settings_path):
            self.create_settings()
        with open(self.settings_path, 'r') as f:
            settings = json.load(f)
        return settings
    
    def create_settings(self) -> None:
        with open(self.settings_path, 'w') as f:
            data = {
                'home': {
                    'latitude': None,
                    'longitude': None,
                },
                'favorites': [],
            }
            json.dump(data, f, indent=4)
            
    def save_settings(self, data: dict[str, dict[str, float | None] | list[list[float]]]) -> None:
        with open(self.settings_path, 'w') as f:
            json.dump(data, f, indent=4)


app = DataManager()
app.get_settings()