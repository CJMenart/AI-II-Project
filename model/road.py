from point import *

class Road:
    def __init__(self, adjHex1, adjHex2, owner):
        self.adjHex1 = adjHex1
        self.adjHex2 = adjHex2
        self.owner = owner
        
    def __eq__(self, other):
        return (self.sameLocationAs(other) and self.owner == other.owner)

    def isOnBoard(self):
        return self.adjHex1.isOnBoard() or \
               self.adjHex2.isOnBoard()

    def sameLocationAs(self, other):
        # the adjHex could be in different order
        return ((self.adjHex1 == other.adjHex1 and self.adjHex2 == other.adjHex2) or \
                    (self.adjHex1 == other.adjHex2 and self.adjHex2 == other.adjHex1) )

    def adjacent(self, r2):
        if (self.adjHex1 == r2.adjHex1):
            return self.adjHex2.adjacent(r2.adjHex2)
        elif (self.adjHex1 == r2.adjHex2):
            return self.adjHex2.adjacent(r2.adjHex1)
        elif (self.adjHex2 == r2.adjHex1):
            return self.adjHex1.adjacent(r2.adjHex2)
        elif (self.adjHex2 == r2.adjHex2):
            return self.adjHex1.adjacent(r2.adjHex1)
        else:
            return False

