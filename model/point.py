class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(a,b):
        return a.x == b.x and a.y == b.y

    def isOnBoard(self):
        return self.x in range(0,5) and \
            self.y in range(0,5) and \
            (self.x+self.y) in range(2,7)

    def allAdjacentPoints(self):
        return [Point(self.x, self.y-1),
                Point(self.x, self.y+1),
                Point(self.x-1, self.y),
                Point(self.x+1, self.y),
                Point(self.x+1, self.y-1),
                Point(self.x-1, self.y+1)]

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

def pointsOnBoard():
    points = []
    for x in range(0,5):
        for y in range(0,5):
            newPoint = Point(x,y)
            if newPoint.isOnBoard():
                points.append(newPoint)
    return points
