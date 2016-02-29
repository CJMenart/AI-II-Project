from point import *

class Road:
    def __init__(self, adjHex1, adjHex2, playerId):
        self.adjHex1 = adjHex1
        self.adjHex2 = adjHex2
        self.playerId = playerId
        
    def __eq__(self, other):
        return (self.adjHex1 == other.adjHex1 and self.adjHex2 == other.adjHex2 and \
                    self.playerId == other.playerId)

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
