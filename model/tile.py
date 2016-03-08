from enum import Enum
from point import Point
from resource import *

class TileType(Enum):
    PASTURE = 1
    HILLS = 2
    MOUNTAINS = 3
    FOREST = 4
    FIELDS = 5
    DESERT = 6

class Tile:
    def __init__(self, tileType, dieNumber):
        self.tileType = tileType
        self.dieNumber = dieNumber

    def resourceTypeProduced(self):
        if (self.tileType == TileType.PASTURE):
            return ResourceType.WOOL
        elif (self.tileType == TileType.HILLS):
            return ResourceType.BRICK
        elif (self.tileType == TileType.MOUNTAINS):
            return ResourceType.ORE
        elif (self.tileType == TileType.FOREST):
            return ResourceType.LUMBER
        elif (self.tileType == TileType.FIELDS):
            return ResourceType.GRAIN
        else:
            return -1; #error
