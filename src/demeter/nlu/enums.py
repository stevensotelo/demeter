from enum import Enum

class Intent(Enum):
    FORECAST_YIELD = 0
    FORECAST_PRECIPITATION = 1
    CLIMATOLOGY = 2
    CULTIVARS = 3
    PLACES = 4
    FORECAST_DATE = 5

    @staticmethod
    def list():
        #return list(map(lambda c: c.name, Intent))
        return dict((label.name, idx) for idx, label in enumerate(Intent))

class Slot(Enum):
    CROP = 0
    CULTIVAR = 1
    LOCALITY = 2
    MEASURE = 3
    DATE = 4
    UNIT = 5

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
    YIELD_PERFORMANCE = 2
    YIELD_DATE = 3

class Error(Enum):
    MISSING_ENTITIES = 0
    MISSING_GEOGRAPHIC = 1
    LOCALITY_NOT_FOUND = 2
    ERROR_ACLIMATE = 3
    ERROR_ACLIMATE_CLIMATOLOGY = 4
    ERROR_ACLIMATE_FORECAST_CLIMATE = 5
    ERROR_ACLIMATE_FORECAST_YIELD = 6
    MISSING_CROP_CULTIVAR = 7

