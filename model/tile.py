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
            return -1 #error

    def numPips(self):
        if self.dieNumber == 2 or self.dieNumber == 12:
            return 1
        elif self.dieNumber == 3 or self.dieNumber == 11:
            return 2
        elif self.dieNumber == 4 or self.dieNumber == 10:
            return 3
        elif self.dieNumber == 5 or self.dieNumber == 9:
            return 4
        elif self.dieNumber == 6 or self.dieNumber == 8:
            return 5
        else:
            return -1 #error
