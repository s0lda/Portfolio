from typing import Any
import geocoder
import geopy

class Location:
    """
    Location from IP address:
        need to work on accuracy
        
    Location from GPS:
        need to add this to the app
    """
    def __init__(self) -> None:
        super().__init__()
        
    def get_usr_location(self) -> list[str] | None:
        '''
        Return the latitude and longitude of the user's IP location
        Return None if the user's IP location is not available,
        usually because the user is not connected to the internet.
        '''
        try:
            location = geocoder.ip('me')
            return location.latlng
        except:
            return None
        
    def find_lat_lon(self, address: str) -> tuple[Any, Any] | None:
        '''
        Return the latitude and longitude of the given address
        Return None if the address is not available,
        usually because the address is not in the database
        eg. wrong address, new address, etc.
        '''
        try:
            geolocator = geopy.Nominatim(user_agent="my-request")
            location = geolocator.geocode(address)
            return location.latitude, location.longitude
        except:
            return None