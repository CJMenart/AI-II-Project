from enum import Enum
from point import Point

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

