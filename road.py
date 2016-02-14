from point import *

class Road:
    def __init__(self, adjHex1, adjHex2):
        self.adjHex1 = adjHex1
        self.adjHex2 = adjHex2

def RoadAdjacent(r1, r2):
    if (r1.adjHex1 == r2.adjHex1):
        return HexAdjacent(r1.adjHex2, r2.adjHex2)
    elif (r1.adjHex1 == r2.adjHex2):
        return HexAdjacent(r1.adjHex2, r2.adjHex1)
    elif (r1.adjHex2 == r2.adjHex1):
        return HexAdjacent(r1.adjHex1, r2.adjHex2)
    elif (r1.adjHex2 == r2.adjHex2):
        return HexAdjacent(r1.adjHex1, r2.adjHex1)
    else:
        return false
