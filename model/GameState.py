from tile import *
from ShuffleBag import ShuffleBag
from point import *
from turn import *
from resource import *
from player import Player
from road import *
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
    #Note that unlike in Chess or Go, the nodes here proceed at an uneven rate. Along
    #some search branches, therefore, five turns may have progressed, while only three
    #have progressed on another branch. This mainly occured because of the robber. BUt
    #the actual build options of the players turn were also coded according to a lens
    #where the number of decision points varies. I haven't yet determined if that's a
    #serious issue.
    def getPossibleNextStates(self):
        newStates = []
        
        if self.turn.turnState == TurnState.DIE_ROLL:
            for num in {1,2,3,4,5,6,8,9,10,11,12}:
                newState = copy.deepcopy(self)
                newState.turn.turnState = TurnState.PLAYER_ACTIONS
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
                            
        elif self.turn.turnState == TurnState.PLAYER_ACTIONS: #the most complicated by far
            newStates.append(self.turn.currentPlayer.buildSomething(self))

        elif self.turn.turnState == TurnState.INITIAL_PLACEMENT:
            for settlement in self.turn.currentPlayer.openSettlementLocations(self):
                #do we also need to make a deep copy of 'settlement'?
                #in theory, we're never going to modify it...
                onBoard1 = settlement.adjHex1.isOnBoard()
                onBoard2 = settlement.adjHex2.isOnBoard()
                onBoard3 = settlement.adjHex3.isOnBoard()

                possibleRoads = []
                if onBoard1 or onBoard2:
                    possibleRoads.append(Road(settlement.adjHex1, settlement.adjHex2, self.turn.currentPlayer))
                if onBoard1 or onBoard3:
                    possibleRoads.append(Road(settlement.adjHex1, settlement.adjHex3, self.turn.currentPlayer))
                if onBoard2 or onBoard3:
                    possibleRoads.append(Road(settlement.adjHex2, settlement.adjHex3, self.turn.currentPlayer))
                
                for road in possibleRoads:
                    newState = copy.deepcopy(self)
                    newState.settlements.append(settlement)
                    newState.roads.append(road)

                    if len(newState.settlements) == 2*len(newState.players):
                        newState.turn.turnState = TurnState.DIE_ROLL
                    elif len(newState.settlements) >= len(newState.players):
                        newState.turn.currentPlayer = newState.previousPlayer()
                    else:
                        newState.turn.currentPlayer = newState.nextPlayer()
                    
                    newStates.append(newState)
                                    
        elif self.turn.turnState == TurnState.MOVE_ROBBER:
            for x in range(0,5):
                for y in range(0,5):
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
                                    if player == victim: #this equality operation should work
                                        player.rmvResource(resource,1)
                                    if player == newState.turn.currentPlayer:
                                        player.addResource(resource,1)
                                newState.turn.turnState = TurnState.PLAYER_ACTIONS
                                newStates.append(newState)
                        
        return newStates

    def nextPlayer(self):
        index = self.players.index(self.turn.currentPlayer)
        index = index + 1
        if index >= len(self.players):
            index = index - len(self.players)
        return self.players[index]

    def previousPlayer(self):
        index = self.players.index(self.turn.currentPlayer)
        index = index - 1
        if index < 0:
            index = index + len(self.players)
        return self.players[index]
            

#Returns a GameState representing a brand-new game
#also providing example of what member data is supposed to look like
def newGame():
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
    numberTokenBag = ShuffleBag([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
    spaces = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],\
             [-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    robberPos = -1


    for x in range(0,5):
        for y in range(0,5):
            if Point(x,y).isOnBoard():
                #TODO: Enforce the rule about red numbers not being next
                #to each other. Is actually a very complex problem
                #and we may not care enough to deal with it
                #We could even do a 'standard' setup version where
                #both numbers and tiles are in fixed position.
                #Might generate a slightly wonkier heuristic tho?
                #Only if we use each separate resource as different
                #inputs to a non-linear heuristic function, perhaps...
                tile = tileBag.next()
                if tile == TileType.DESERT:
                    robberPos = Point(x,y)
                    spaces[x][y] = Tile(tile, -1)
                else:
                    spaces[x][y] = Tile(tile, numberTokenBag.next())

    #Game begins with no roads or settlements in play
    settlements = []
    roads = []

    #initialize players...and then
    players = []
    for player in range(0,3):
        players.append(Player(player, {ResourceType.WOOL:0, ResourceType.BRICK:0,
                                       ResourceType.ORE:0, ResourceType.LUMBER:0, ResourceType.GRAIN:0}))

    #construct the turn data with a randomly-selected player
    turn = Turn(TurnState.INITIAL_PLACEMENT, players[0])
    
    return GameState(spaces, players, roads, settlements, robberPos, turn)

