from HexTile import HexTile
from ShuffleBag import ShuffleBag

#anything in this file can still be refactored and shufled around. Just
#trying to sort things out

class GameState:
    #Tentative data members:
    #spaces: grid keeping track of hex types/numbers
    #players: list of structures with info like hands, color, etc.
    #peices: list of wooden peices like settlements, roads, roobers, with
    #       their positions
    #Turn: info specifying at what point in time of gameplay we're at.
    
    #Two constructors: a copy constructor and one that passes in all data
    #variables individually

    def __init__(self, spaces, players, peices, turn):
        self.spaces = spaces
        self.players = players
        self.peices = peices
        self.turn = turn

    def __init__(self, otherGameState):
        self.spaces = otherGameState.spaces
        self.players = otherGameState.players
        self.peices = otherGameState.peices
        self.turn = otherGameState.turn

    def HexAdjacent(self, x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2

        if dx == 0 and abs(dy) == 1:
            return true
        if dy == 0 and abs(dx) == 1:
            return true
        if abs(dx) == 1 and dy == -dx:
            return true

        return false

#Returns a GameState representing a brand-new game
#also providing example of what member data is supposed to look like
def NewGame():
    tileBag = ShuffleBag([TileType.PASTURE,
                          TileType.PASTURE,
                          TileType.PASTURE,
                          TileType.PASTURE,
                          TileType.FOREST,
                          TileType.FOREST,
                          TileType.FOREST,
                          TileType.FOREST,
                          TileType.HILLS,
                          TileType.HILLS,
                          TileType.HILLS,
                          TileType.MOUNTAINS,
                          TileType.MOUNTAINS,
                          TileType.MOUNTAINS,
                          TileType.FIELDS,
                          TileType.FIELDS,
                          TileType.FIELDS,
                          TileType.FIELDS,
                          TileType.DESERT])
    numberTokenBag = ShufleBag([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
    spaces = [[],[],[],[],[]]

    for x in range(0,4):
        for y in range(0,4):
            if (x+y) > 6 or (x+y) < 2: #then these indices are off the board
                spaces[x,y] = -1
            else:
                spaces[x,y] = HexTile(tileBag.next(), numberTokenBag.next())

    return GameState(spaces, players, peices, turn)

    #some stuff...and then

    

    #TODO: incomplete function
