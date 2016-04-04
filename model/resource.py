# We want enum34 in order to support iteration over ResourceType
from enum import IntEnum

class ResourceType(IntEnum):
    WOOL = 1
    BRICK = 2
    ORE = 3
    LUMBER = 4
    GRAIN = 5
