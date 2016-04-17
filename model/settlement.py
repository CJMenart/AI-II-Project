from point import *
from road import *


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
                    True if self.owner <0 else self.owner == other.owner)
    
    def __hash__(self):
        return (self.adjHex1.x + self.adjHex2.y) * (self.adjHex3.x+2) 

    def __str__(self):
        return ("adjHex1: {0}, adjHex2: {1}, adjHex3: {2} owner: {3}".format( \
                self.adjHex1, self.adjHex2, self.adjHex3, self.owner))

    def isOnBoard(self):
        return self.adjHex1.isOnBoard() or \
               self.adjHex2.isOnBoard() or \
               self.adjHex3.isOnBoard()

    def sumHexes(self):
        return self.adjHex1 + self.adjHex2 + self.adjHex3

    @staticmethod
    def hexToTLCorner(pt):
        x = pt.x
        y = pt.y
        return Point(2*x+y-2, y-x+5)

    def lowerRightHex(self):
        sumHex = self.sumHexes()
        xMod = sumHex.x % 3
        yMod = sumHex.y % 3
        assert(xMod == yMod)
        if xMod == 2:
            # up
            off = Point(1,1)
        else:
            off = Point(-1,2)
        return (sumHex + off)/3

    def toCorner(self):
        return hexToTLCorner(self.lowerRightHex())

    @staticmethod
    def isCorner(pt):
        return pt.x>=0 and pt.x<11 and pt.y>=0 and pt.y<11 and pt.x+pt.y>=5 and pt.x+pt.y<=15 and (pt.x % 5 != 0 or pt.y % 5 != 0)

    # True if the edges at this vertex look like a Y
    @staticmethod
    def isUp(pt):
       return (pt.x-pt.y+7) % 3 == 0

    @staticmethod
    def cornerToHex(pt, isUp):
        if isUp:
            hx = (pt.x-pt.y+7)/3
            hy = pt.y + hx
        else:
            hx = (pt.x-pt.y+5)/3
            hy = pt.y + hx + 1
        return Point(hx, hy)

    # TODO: test
    @staticmethod
    def getAdjHexes(pt):
        assert(isCorner(pt))
        off1 = Point(0,-1)
        if isUp(pt):
            hex1 = cornerToHex(pt, True)
            off2 = Point(-1,0)
        else:
            assert((pt.x-pt.y+5) % 3 == 0)
            hex1 = cornerToHex(pt, False)
            off2 = Point(1,-1)
        return [hex1, hex1+off1, hex1+off2]

    # TODO: test
    @staticmethod
    def getAdjVertices(pt):
        adj = []
        offs = [Point(-1,0), Point(1,-1), Point(0,1)]
        up = isUp(pt)
        for off in offs:
            if up:
                pt2 = pt + off
            else:
                pt2 = pt - off
            if isCorner(pt2):
                adj.append(pt2)
        return adj

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

    def adjacentSettlements(self):
        adjRoads = self.adjacentRoads()
        adjSettlements = []
        for r in adjRoads: 
            for s in Settlement.adjacentSettlementsByRoad(r): 
                if ((s not in adjSettlements) and (s != self)): 
                    adjSettlements.append(s)
        return adjSettlements

    def getSettlementWithOwner(self, id): 
        if self.owner < 0 :
            return Settlement(self.adjHex1, self.adjHex2, self.adjHex3, id)
        else:
            print("Error: attempting to change road owner")

    def levelOfIncome(self, gameState):
        income = 0
        for adjHex in {self.adjHex1, self.adjHex2, self.adjHex3}:
                if adjHex.isOnBoard() and not gameState.robberPos == adjHex:
                    income += gameState.spaces[adjHex.x][adjHex.y].numPips() * (2 if self.isCity else 1)
        return income

    @classmethod
    def adjacentSettlementsByRoad(cls, road):
        # take intersection of two adjacent Points set will get two close points                 
        adjHex1adjPoints = road.adjHex1.allAdjacentPoints()
        adjHex2adjPoints = road.adjHex2.allAdjacentPoints()
        twoClosePoints = list(set(adjHex1adjPoints).intersection(adjHex2adjPoints))
        return [Settlement(twoClosePoints[0], road.adjHex1, road.adjHex2, -1), \
                   Settlement(twoClosePoints[1], road.adjHex1, road.adjHex2, -1)]
