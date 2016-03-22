from point import *

class Settlement:
    def __init__(self, adjHex1, adjHex2, adjHex3, owner):
        self.adjHex1 = adjHex1
        self.adjHex2 = adjHex2
        self.adjHex3 = adjHex3
        self.isCity = False
        self.owner = owner

    def __eq__(self, other): 
        return (self.adjHex1 in [other.adjHex1, other.adjHex2, other.adjHex3] and \
                    self.adjHex1 in[other.adjHex1, other.adjHex2, other.adjHex3] and \
                    self.adjHex1 in[other.adjHex1, other.adjHex2, other.adjHex3] and \
                    self.owner == other.owner)

    def isOnBoard(self):
        return self.adjHex1.isOnBoard() or \
               self.adjHex2.isOnBoard() or \
               self.adjHex3.isOnBoard()

    def adjacentOrCloser(self, s2):
        adjacencies = 0

        if (self.adjHex1 == s2.adjHex1):
            adjacencies += 1
        if (self.adjHex1 == s2.adjHex2):
            adjacencies += 1
        if (self.adjHex1 == s2.adjHex3):
            adjacencies += 1
        if (self.adjHex2 == s2.adjHex2):
            adjacencies += 1
        if (self.adjHex2 == s2.adjHex3):
            adjacencies += 1
        if (self.adjHex3 == s2.adjHex3):
            adjacencies += 1
        
        return adjacencies >= 2

