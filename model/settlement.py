from point import *
from road import Road

class Settlement:
    def __init__(self, adjHex1, adjHex2, adjHex3, owner):
        if (adjHex1 != adjHex2 and adjHex1 != adjHex3 and adjHex2 != adjHex3):
            self.adjHex1 = adjHex1
            self.adjHex2 = adjHex2
            self.adjHex3 = adjHex3
            self.isCity = False
            self.owner = owner
        else: 
            print("Error. Initializing settlemnt with identical adjHexes")

    def __eq__(self, other): 
        return (self.adjHex1 in [other.adjHex1, other.adjHex2, other.adjHex3] and \
                    self.adjHex2 in[other.adjHex1, other.adjHex2, other.adjHex3] and \
                    self.adjHex3 in[other.adjHex1, other.adjHex2, other.adjHex3] and \
                    self.owner == other.owner)

    def isOnBoard(self):
        return self.adjHex1.isOnBoard() or \
               self.adjHex2.isOnBoard() or \
               self.adjHex3.isOnBoard()

    def adjacentOrCloser(self, s2):
        adjacencies = 0

        s2Hexes = {s2.adjHex1, s2.adjHex2, s2.adjHex3}

        if (self.adjHex1 in s2Hexes):
            adjacencies += 1
        if (self.adjHex2 in s2Hexes):
            adjacencies += 1
        if (self.adjHex3 in s2Hexes):
            adjacencies += 1
        
        return adjacencies >= 2

    def adjacentRoads(self): 
        return [Road(self.adjHex1, self.adjHex2, -1), \
                    Road(self.adjHex1, self.adjHex3, -1), \
                    Road(self.adjHex2, self.adjHex3, -1)]

