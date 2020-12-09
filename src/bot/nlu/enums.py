from enum import Enum

class Intent(Enum):
    FORECAST_CROP_YIELD = 0
    FORECAST_CLIMATE = 1
    HISTORICAL_CLIMATOLOGY = 2
    LIST_CULTIVARS = 3
    LIST_PLACES = 4
    FORECAST_CROP_DATE = 5

    @staticmethod
    def list():
        
        #return list(map(lambda c: c.name, Intent))
        return dict((label.name, idx) for idx, label in enumerate(Intent))

class Slot(Enum):
    PAD = 0
    CROP = 1
    B_CULTIVAR = 2
    I_CULTIVAR = 3
    B_LOCALITY = 4
    I_LOCALITY = 5
    B_MEASURE = 6
    I_MEASURE = 7
    B_DATE = 8
    I_DATE = 9
    B_UNIT = 10
    I_UNIT = 11
    O = 12

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

