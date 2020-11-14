from enum import Enum

class Intent(Enum):
    LIST_CULTIVARS = 1
    LIST_PLACES = 2
    FORECAST_CLIMATE = 3
    HISTORICAL_CLIMATOLOGY = 4

class Geographic(Enum):
    STATE = 1
    MUNICIPALITIES_STATE = 2
    WS_MUNICIPALITY = 3
    WEATHER_STATION = 4

class Cultivars(Enum):
    CROP_MULTIPLE = 1    
    CROP_CULTIVAR = 2
    CULTIVARS_MULTIPLE = 3

class Forecast(Enum):
    CLIMATE = 1

class Historical(Enum):
    CLIMATOLOGY = 1
