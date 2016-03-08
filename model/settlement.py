from point import *

class Settlement:
    def __init__(self, adjHex1, adjHex2, adjHex3, owner):
        self.adjHex1 = adjHex1
        self.adjHex2 = adjHex2
        self.adjHex3 = adjHex3
        self.isCity = False
        self.owner = owner

    def __eq__(self, other): 
        return (self.adjHex1 == other.adjHex1 and \
                    self.adjHex2 == other.adjHex2 and \
                    self.adjHex3 == other.adjHex3 and \
                    self.owner == other.owner)

    def isOnBoard(self):
        return self.adjHex1.isOnBoard() OR \
               self.adjHex2.isOnBoard() OR \
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

