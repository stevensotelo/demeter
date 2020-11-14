from enum import Enum

class Intent(Enum):
    LIST_CULTIVARS = 1
    LIST_PLACES = 2

class Geographic(Enum):
    STATE = 1
    MUNICIPALITIES_STATE = 2
    WS_MUNICIPALITY = 3
    WEATHER_STATION = 4

class Cultivars(Enum):
    CROP_MULTIPLE = 1    
    CROP_CULTIVAR = 2
    CULTIVARS_MULTIPLE = 3

class ClimateForecast(Enum):
    CLIMATE = 1
    ENTITIES_NOT_FOUND = 2
    LOCALITIES_NOT_FOUND = 3
