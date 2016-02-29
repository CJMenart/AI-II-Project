from point import *

class Settlement:
    def __init__(self, adjHex1, adjHex2, adjHex3):
        self.adjHex1 = adjHex1
        self.adjHex2 = adjHex2
        self.adjHex3 = adjHex3
        self.isCity = False

    def isOnBoard(self):
        return self.adjHex1.isOnBoard() OR \
               self.adjHex2.isOnBoard() OR \
               self.adjHex3.isOnBoard()

def SettlementAdjacent(s1, s2):
    adjacencies = 0

    if (s1.adjHex1 == s2.adjHex1):
        adjacencies += 1
    if (s1.adjHex1 == s2.adjHex2):
        adjacencies += 1
    if (s1.adjHex1 == s2.adjHex3):
        adjacencies += 1
    if (s1.adjHex2 == s2.adjHex2):
        adjacencies += 1
    if (s1.adjHex2 == s2.adjHex3):
        adjacencies += 1
    if (s1.adjHex3 == s2.adjHex3):
        adjacencies += 1
    
    return adjacencies >= 2
