class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(a,b):
        return a.x == b.x and a.y == b.y

    def __str__(self):
        return ('({0}, {1})'.format(self.x, self.y))
    
    def __hash__(self):
        return hash((self.x, self.y))

    def isOnBoard(self):
        return self.x in range(0,5) and \
            self.y in range(0,5) and \
            (self.x+self.y) in range(2,7)

    def __add__(self, h2):
        return Point(self.x + h2.x, self.y + h2.y)

    def __sub__(self, h2):
        return Point(self.x - h2.x, self.y - h2.y)

#    directions = [Point( 1,-1), Point( 0,-1), Point(-1, 0), Point(-1, 1), Point( 0, 1), Point( 1, 0)]

    # these are in counter-clockwise order starting from 0 degrees for convenience with angles
    def allAdjacentPoints(self):
        return [Point(self.x+1, self.y-1),
                Point(self.x  , self.y-1),
                Point(self.x-1, self.y  ),
                Point(self.x-1, self.y+1),
                Point(self.x  , self.y+1),
                Point(self.x+1, self.y  )]
                # DON'T need to account for offset layout (we are using axial coordinates)
                #Point(self.x-1, self.y-1+2*(self.x%2) ),
                #Point(self.x+1, self.y-1+2*(self.x%2) )

    #Takes two Points
    def adjacent(self, h2):
        dx = self.x - h2.x
        dy = self.y - h2.y

        if dx == 0 and abs(dy) == 1:
            return True
        if dy == 0 and abs(dx) == 1:
            return True
        if abs(dx) == 1 and dy == -dx:
            return True

        return False

point_directions = Point(0,0).allAdjacentPoints()

def pointsOnBoard():
    points = []
    for x in range(0,5):
        for y in range(0,5):
            newPoint = Point(x,y)
            if newPoint.isOnBoard():
                points.append(newPoint)
    return points
