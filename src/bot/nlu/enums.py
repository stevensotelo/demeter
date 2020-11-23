from enum import Enum

class Intent(Enum):
    LIST_CULTIVARS = 1
    LIST_PLACES = 2    
    HISTORICAL_CLIMATOLOGY = 3
    FORECAST_CLIMATE = 4
    FORECAST_CROP_YIELD = 5
    FORECAST_CROP_DATE = 6

class Geographic(Enum):
    STATE = 1
    MUNICIPALITIES_STATE = 2
    WS_MUNICIPALITY = 3
    WEATHER_STATION = 4

class Cultivars(Enum):
    CROP_MULTIPLE = 1    
    CROP_CULTIVAR = 2
    CULTIVARS_MULTIPLE = 3

class Historical(Enum):
    CLIMATOLOGY = 1

class Forecast(Enum):
    CLIMATE = 1

class Error(Enum):
    MISSING_GEOGRAPHIC = 1
    LOCALITY_NOT_FOUND = 2

