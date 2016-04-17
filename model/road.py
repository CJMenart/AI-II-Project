from point import *

class Road:
    def __init__(self, adjHex1, adjHex2, owner):
        if (adjHex1 != adjHex2):
            self.adjHex1 = adjHex1
            self.adjHex2 = adjHex2
            self.owner = owner
        else: 
            print("Error! initlalizing road with identical adjHexes")
        
    def __eq__(self, other):
        # use negative owner number as a wildcard 
        return (self.sameLocationAs(other) and \
                    True if self.owner <0 or  other.owner < 0 \
                    else self.owner == other.owner)

    def __str__(self):
        return ("adjHex1: {0}, adjHex2: {1}, owner: {2}".format(self.adjHex1, self.adjHex2, self.owner))

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

    def adjacentRoads(self):
        # take intersection of two adjacent Points set will get two close points
        adjHex1adjPoints = self.adjHex1.allAdjacentPoints()
        adjHex2adjPoints = self.adjHex2.allAdjacentPoints()
        twoClosePoints = list(set(adjHex1adjPoints).intersection(adjHex2adjPoints))
        
        return [Road(twoClosePoints[0], self.adjHex1, -1), \
                    Road(twoClosePoints[0], self.adjHex2, -1), \
                    Road(twoClosePoints[1], self.adjHex1, -1), \
                    Road(twoClosePoints[1], self.adjHex2, -1)]

    def getRoadWithOwner(self, id):
        return Road(self.adjHex1, self.adjHex2, id)



