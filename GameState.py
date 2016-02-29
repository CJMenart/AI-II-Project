from tile import Tile
from shuffleBag import ShuffleBag
from point import Point
from turn import Turn

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
        self.spaces = list(otherGameState.spaces) #deep enough. We don't change these
        self.players = list(otherGameState.players) #need deeper copy?
        self.peices = list(otherGameState.peices) #need deeper copy? We may modify settlements...
        self.turn = Turn(otherGameState.turn) #deep enough

    #gets child nodes on down the H-Minimax graph
    def getPossibleNextStates(self):
        newStates = []
        
        if turn.turnState == TurnState.DIE_ROLL:
        elif turn.turnState == TurnState.PLAYER_ACTIONS: #the most complicated by far
        elif turn.turnState == TurnState.INITIAL_PLACEMENT:
            for x in range(0,4):
                for y in range(0,4):
                    basePoint = Point(x,y)
                    if basePoint.isOnBoard():
                        for point2 in basePoint.AllAdjacentPoints():
                            for point3 in [val for val in \
                                    basePoint.AllAdjacentPoints() if \
                                    val in point2.AllAdjacentPoints()]:
                                settlement = Settlement(basePoint, point2, point3)
                                if settlement not in self.pieces:
                                    #do we also need to make a deep copy of 'settlement'?
                                    #in theory, we're never going to modify it...
                                    state1 = self.Copy()
                                    state1.peices.append(settlement, Road(basePoint, point2))
                                    newStates.append(state1)

                                    state2 = self.Copy()
                                    state2.peices.append(settlement, Road(basePoint, point3))
                                    newStates.append(state2)

                                    state3 = self.Copy()
                                    state3.peices.append(settlement, Road(point2, point3))
                                    newStates.append(state1)

        return newStates
    
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
            if not Point(x,y).isOnBoard(): #then these indices are off the board
                spaces[x][y] = -1
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
                    spaces[x][y] = Tile(tile, -1)
                else:
                    spaces[x][y] = Tile(tile, numberTokenBag.next())

    #Game begins with no roads or settlements in play
    peices = []

    #initialize players...and then


    #construct the turn data with a randomly-selected player
    turn = Turn(TurnState.INITIAL_PLACEMENT, randPlayer)

    
    
    return GameState(spaces, players, peices, robberPos, turn)


    

    #TODO: incomplete function

