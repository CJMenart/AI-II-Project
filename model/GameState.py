from tile import Tile
from ShuffleBag import ShuffleBag
from point import Point
from turn import Turn
from resource import *
import copy

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

    def __init__(self, spaces, players, roads, settlements, robberPos, turn):
        self.spaces = spaces
        self.players = players
        self.roads = roads
        self.settlements = settlements
        self.turn = turn
        self.robberPos = robberPos;
  
    #gets child nodes on down the H-Minimax graph
    def getPossibleNextStates(self):
        newStates = []
        
        if turn.turnState == TurnState.DIE_ROLL:
            for num in {1,2,3,4,5,6,8,9,10,11,12}:
                newState = copy.deepcopy(self)
                for settlement in newState.settlement:
                    for point in {settlement.adjHex1, settlement.adjHex2,settlement.adjHex3}:
                        if newState.spaces[point.x, point.y].dieNumber == num:
                            settlement.owner.addResource(
                                newState.spaces[point.x,point.y].resourceTypeProduced(),
                                2 if settlement.isCity else 1)
                            newStates.append(newState)

            #then add the state where you roll a 7
            newState = copy.deepcopy(self)
            newState.turn.turnState = TurnState.MOVE_ROBBER
                            
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
                                legalPlace = True
                                if settlement in self.settlements:
                                    legalPlace = False
                                for existingSettlement in self.settlements:
                                    if settlementAdjacent(settlement, existingSettlement):
                                        legalPlace = False
                                if legalPlace:
                                    #do we also need to make a deep copy of 'settlement'?
                                    #in theory, we're never going to modify it...
                                    state1 = copy.deepcopy(self)
                                    state1.settlements.append(settlement)
                                    state1.roads.append(Road(basePoint, point2))
                                    newStates.append(state1)

                                    state2 = copy.deepcopy(self)
                                    state2.settlements.append(settlement)
                                    state2.roads.append(Road(basePoint, point3))
                                    newStates.append(state2)

                                    state3 = copy.deepcopy(self)
                                    state3.settlements.append(settlement)
                                    state3.roads.append(Road(point2, point3))
                                    newStates.append(state3)
                                    
        elif turn.turnState == TurnState.MOVE_ROBBER:
            for x in range(0,4):
                for y in range(0,4):
                    point = Point(x,y)
                    if not point.isOnBoard() or point == robberPos:
                        continue
                    
                    #Who can you steal from if you place the robber in this spot?
                    robbablePlayers = []
                    for settlement in self.settlements:
                        if point in {settlements.adjHex1, settlements.adjHex2,
                                     settlements.adjHex3}:
                            if settlement.owner not in robbablePlayers:
                                robbablePlayers.append(settlement.owner)

                    #Note that this exludes the POSSIBILITY of placing the robber
                    #where it doesn't steal from anyone. Though technically this is
                    #possible withint the rules, if players are playing a normal game
                    #this never happens, so it's probably an acceptable simplification
                    for victim in robbablePlayers:
                        for resource in ResourceType:
                            if victim.resources[resource] > 0:
                                #now we know exactly the specification of one possible choice
                                newState = copy.deepcopy(self)
                                newState.robberPos = point
                                for player in newState.players:
                                    if player == victim:
                                        player.rmvResource(resource,1)
                                    if player == newState.turn.currentPlayer:
                                        player.addResource(resource,1)
                                newState.turn.turnState = TurnState.PLAYER_ACTIONS
                                newStates.append(newState)
                        
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
    players = []
    for player in range(0,3):
        players.append(Player(player, {ResourceType.WOOL:0, ResourceType.BRICK:0,
                                       ResourceType.ORE:0, ResourceType.LUMBER:0, ResourceType.GRAIN:0}))

    #construct the turn data with a randomly-selected player
    turn = Turn(TurnState.INITIAL_PLACEMENT, players[0])
    
    return GameState(spaces, players, peices, robberPos, turn)

