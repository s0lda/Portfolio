import csv
from math import pi, sin, cos, sqrt, asin

class AirportDistanceChecker():
    def __init__(self, database: str) -> None:
        self._db = database
        self.airports = self.get_airports_list()
        
    def get_airport_distance(self, airport_1: tuple[str, str], airport_2: tuple[str, str]) -> float:
        '''Return the distance between two airports in kilometers.
        
        >>> airport_1 = (latitude deg, longitute deg)
        >>> airport_2 = (latitude deg, longitute deg)'''
        airport_1_lat = float(airport_1[0])
        airport_1_lon = float(airport_1[1])
        airport_2_lat = float(airport_2[0])
        airport_2_lon = float(airport_2[1])
        # convert to radians
        airport_1_lat = airport_1_lat * pi / 180
        airport_1_lon = airport_1_lon * pi / 180
        airport_2_lat = airport_2_lat * pi / 180
        airport_2_lon = airport_2_lon * pi / 180
        # calculate distance
        d_lat = airport_2_lat - airport_1_lat
        d_lon = airport_2_lon - airport_1_lon
        a = sin(d_lat / 2)**2 + cos(airport_1_lat) * cos(airport_2_lat) * sin(d_lon / 2)**2
        c = 2 * asin(sqrt(a))
        km: float = 6371 * c
        return round(km, 2)
    
    def get_airport_details(self, airport_name: str) -> list[str] | None:
        '''Return a list with airport details if airport_name is found in the database.
        
        >>> name, latitude deg, longitute deg, IATA code, country, municipality'''
        for airport in self.airports:
            if airport[0].lower() == airport_name.lower() or airport[3].lower() == airport_name.lower():
                return airport
        return None
    
    def get_airports_list(self) -> list[list[str]]:
        '''Return a list of all airports in the database with IATA code and coordinates.
        
        >>> name, latitude deg, longitute deg, IATA code, country, municipality'''
        airports_list = []
        with open(self._db, newline='', encoding='utf-8') as file:
            data = csv.reader(file, delimiter=',', quotechar='"')
            for row in data:
                airport_data = [row[3], row[4], row[5], row[13], row[8], row[10]]
                airports_list.append(airport_data) # type: ignore
        iata_airports: list[list[str]] = []
        for airport in airports_list: # type: ignore
            if airport[3] == '':
                pass
            else:
                iata_airports.append(airport) # type: ignore
        # remove heading
        iata_airports.remove(iata_airports[0])  # type: ignore
        return iata_airports
            
        
# app = AirportDistanceChecker(
#     database='C://Users/Komputer/Documents/GitHub/Portfolio/kivy_apps/Airport_Dist_Calc/res/airports.csv')
# print(app.get_airport_details('BRS'))
# print(app.get_airport_details('MDL'))
# print(app.get_airport_distance(('51.382702', '-2.71909'), ('21.702199935913086', '95.97789764404297',)))