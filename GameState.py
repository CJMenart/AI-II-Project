from tile import Tile
from shuffleBag import ShuffleBag
from point import Point

#anything in this file can still be refactored and shufled around. Just
#trying to sort things out

class GameState:
    #Tentative data members:
    #spaces: grid keeping track of hex types/numbers
    #players: list of structures with info like hands, color, etc.
    #peices: list of wooden peices like settlements, roads, with
    #       their positions
    #Turn: info specifying at what point in time of gameplay we're at.
    
    #Two constructors: a copy constructor and one that passes in all data
    #variables individually

    def __init__(self, spaces, players, peices, robberPos, turn):
        self.spaces = spaces
        self.players = players
        self.peices = peices
        self.turn = turn
        self.robberPos;

    def __init__(self, otherGameState):
        self.spaces = otherGameState.spaces
        self.players = otherGameState.players
        self.peices = otherGameState.peices
        self.turn = otherGameState.turn

  

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
                #TODO: Enforce the rule about red numbers not being next
                #to each other. Is actually a very complex problem
                #and we may not care enough to deal with it
                #We could even do the 'standard' setup version where
                #both numbers and tiles are in fixed position.
                #Might generate a slightly wonkier heuristic tho?
                tile = tileBag.next();
                if tile == TileType.DESERT:
                    robberPos = Point(x,y)
                    spaces[x,y] = Tile(tile, -1)
                else:
                    spaces[x,y] = Tile(tile, numberTokenBag.next())

    #Game begins with no roads or settlements in play
    peices = []

    #initialize players...and then


    #construct the turn data with a randomly-selected player
    turn = Turn(TurnState.INITIAL_PLACEMENT, randPlayer)

    
    
    return GameState(spaces, players, peices, robberPos, turn)


    

    #TODO: incomplete function

