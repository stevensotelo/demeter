from enum import Enum

class Intent(Enum):
    LIST_CULTIVARS = 1
    LIST_PLACES = 2

class Geographic(Enum):
    STATE = 1
    MUNICIPALITY = 2
    LOCALITY = 3

class Cultivars(Enum):
    CROP = 1
    CULTIVARS = 2
