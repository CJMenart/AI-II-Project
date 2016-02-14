class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(a,b):
        return a.x == b.x and a.y == b.y

    def isOnBoard(self):
        return self.x in range(0,4) and \
            self.y in range(0,4) and \
            (self.x+self.y) in range(2,6)

#Takes two Points
def HexAdjacent(h1, h2):
    dx = h1.x - h2.x
    dy = h1.y - h2.y

    if dx == 0 and abs(dy) == 1:
        return True
    if dy == 0 and abs(dx) == 1:
        return True
    if abs(dx) == 1 and dy == -dx:
        return True

    return False
