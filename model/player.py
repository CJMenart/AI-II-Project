# this file defines player class that packages player associated data 
# and behavior

#IMPORTNAT NOTE: As of now, SOME player functions cause in-place changse
#to the player objects. Others return new states. It's not immediately
#clear which is which. Possibly this should be addressed and refactored,
#but I've been refactoring all day, so I'm not changing it now...

#from enum import Enum
from resource import *
from point import *
from settlement import *
from road import *
from turn import *
import copy

class Player:
    def __init__(self, inputPlayerId, resources = {ResourceType.WOOL: 0 , ResourceType.BRICK:0, \
                ResourceType.ORE:0, ResourceType.LUMBER:0, ResourceType.GRAIN:0}  ):
        self.playerId = inputPlayerId
        self.resources =copy.deepcopy(resources)
        #below: what a basic player with an empty hand looks like
        #self.resources = {ResourceType.WOOL: 0 , ResourceType.BRICK:0,
        #ResourceType.ORE:0, ResourceType.LUMBER:0, ResourceType.GRAIN:0}

    def __eq__(self, other):
        return self.playerId == other.playerId

    def addResource(self, resourceType, nResource):
        self.resources[resourceType] += nResource
        return 0 # means success                                                                    

    def rmvResource(self, resourceType, nResource):
        if nResource > self.resources[resourceType]:
            return 1 # means error cannot remove more than what already have                    
        else:
            self.resources[resourceType] -= nResource
            return 0

    # count the number of resource cards                                                        
    def nResources(self):
        return sum(self.resources.values())

    # return a list of roads that belongs to the player                                            
    def roads(self, gameState):
        playerRoads =[]
        for r in gameState.roads:
            if r.owner == self.playerId:
                playerRoads.append(r)
        return playerRoads

    # get a list of settlements that belong to the player                                        
    def settlements(self, gameState):
        playerSettlements = []
        for s in gameState.settlements:
            if s.owner == self.playerId:
                playerSettlements.append(s)
        return playerSettlements

    def numBasicSettlements(self, gameState):
        num = 0
        for settlement in self.settlements(gameState):
            if not settlement.isCity:
                num += 1
        return num

    def numCities(self, gameState):
        num = 0
        for settlement in self.settlements(gameState):
            if settlement.isCity:
                num += 1
        return num

    def numCards(self):
        res = self.resources
        return res[ResourceType.ORE] + res[ResourceType.WOOL] + \
            res[ResourceType.LUMBER] + res[ResourceType.GRAIN] + \
            res[ResourceType.BRICK]


    #returns a list of roads
    #may return duplicates
    def openRoadLocations(self,gameState):
        openLocations = []
        for basePoint in pointsOnBoard():
            for point2 in basePoint.allAdjacentPoints():
                road = Road(basePoint, point2, self.playerId)
                legalPlacement = True
                for existingRoad in gameState.roads:
                    if road.sameLocationAs(existingRoad):
                        legalPlacement = False
                if legalPlacement:
                    openLocations.append(road)
        return openLocations


    # get a list of available roads that the player could build
    def availableRoads(self, gameState):
        buildableRoads = []
        '''
        for road in self.openRoadLocations(gameState):
            #Now we need to check if you have another road
            #adjacent to this one
            for existingRoad in self.roads(gameState):
                if basePoint == existingRoad.adjHex1:
                    if point2.adjacent(existingRoad.adjHex2):
                        buildableRoads.append(road)
                if basePoint == existingRoad.adjHex2:
                    if point2.adjacent(existingRoad.adjHex1):
                        buildableRoads.append(road)
        '''
        for s in self.settlements(gameState):
            for closeRoad in s.adjacentRoads():
                if closeRoad.isOnBoard() and closeRoad not in gameState.roads: 
                    buildableRoads.append(closeRoad)
        for r in self.roads(gameState):
            for closeRoad in r.adjacentRoads():
                #for mr in r.adjacentRoads():
                #    print(mr)
                if closeRoad.isOnBoard() and closeRoad not in gameState.roads and \
                        closeRoad not in buildableRoads:
                    buildableRoads.append(closeRoad)
            
        return buildableRoads

    #returns a list of settlements
    #may return duplicates
    def openSettlementLocations(self, gameState):
        openLocations = []
        for basePoint in pointsOnBoard():
            basePointNbors = basePoint.allAdjacentPoints()
            for point2 in basePointNbors:
                for point3 in [val for val in \
                                basePointNbors if \
                                val in point2.allAdjacentPoints()]:
                    settlement = Settlement(basePoint, point2, point3, self.playerId)
                    #check whether an existing settlement is in the same
                    #space or adjacent
                    legalPlacement = True
                    for existingSettlement in gameState.settlements:
                        if settlement.adjacentOrCloser(existingSettlement):
                            legalPlacement = False
                    if legalPlacement:
                        openLocations.append(settlement)
        return openLocations

    
    # get a list of available settlements that the player could build
    def availableSettlements(self, gameState):
        buildableSettlements = []
        '''
        for settlement in self.openSettlementLocations(gameState):
            for road in self.roads(gameState):
                if road.adjHex1 in {settlement.adjHex1, settlement.adjHex2, settlement.adjHex3} and \
                        road.adjHex2 in {settlement.adjHex1, settlement.adjHex2, settlement.adjHex3}:
                    buildableSettlements.append(settlement)
                    break
        '''
        for r in self.roads(gameState):
            for s in Settlement.adjacentSettlementsByRoad(r):
                # check if duplicate,violate with existing settle, or adjacent to existing settlements
                if s not in buildableSettlements and s not in gameState.settlements and \
                        s not in [item for sublist in list(map(lambda x:x.adjacentSettlements(),gameState.settlements)) for item in sublist]: 
                    buildableSettlements.append(s)
        return buildableSettlements

    #returns the child nodes of a GameState in which this player takes zero or one build options
    def buildSomething(self, gameState):
        possibleNextStates = []
        
        #the first state represents doing nothing.
        passTurn = copy.deepcopy(gameState)
        passTurn.turn.currentPlayer = passTurn.nextPlayer()
        passTurn.turn.turnState = TurnState.DIE_ROLL
        passTurn.turn.turnNumber += 1
        possibleNextStates.append(passTurn)

        #from there, we create states representing:
        #can you trade 4 resources to the bank to get a resource of your choice?
        stateIndex = 0
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            for fromIndex in ResourceType:
                if state.getPlayerByIndex(state.turn.currentPlayer).resources[fromIndex] >= 4:
                    for toIndex in [i for i in ResourceType if i != fromIndex]:
                        traded = copy.deepcopy(state)
                        traded.getPlayerByIndex(traded.turn.currentPlayer).resources[fromIndex] -= 4
                        traded.getPlayerByIndex(traded.turn.currentPlayer).resources[toIndex] += 1
                        possibleNextStates.append(traded)
            stateIndex += 1

        #from there:
        #can you build a road?
        stateIndex = 0
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            player = state.getPlayerByIndex(state.turn.currentPlayer)
            if player.resources[ResourceType.BRICK] >= 1 and \
                   player.resources[ResourceType.LUMBER] >= 1:
                for road in player.availableRoads(state):
                    builtRoad = copy.deepcopy(state)
                    builtRoad.roads.append(road.getRoadWithOwner(player.playerId))
                    builtRoad.getPlayerByIndex(builtRoad.turn.currentPlayer).resources[ResourceType.BRICK] -= 1
                    builtRoad.getPlayerByIndex(builtRoad.turn.currentPlayer).resources[ResourceType.LUMBER] -= 1
                    possibleNextStates.append(builtRoad)
            stateIndex += 1

        #can you build a settlement?
        stateIndex = 0
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            player = state.getPlayerByIndex(state.turn.currentPlayer)

            if player.resources[ResourceType.BRICK] >= 1 and \
                    player.resources[ResourceType.LUMBER] >= 1 and \
                    player.resources[ResourceType.WOOL] >= 1 and \
                    player.resources[ResourceType.GRAIN] >= 1 and player.numBasicSettlements(gameState) < 5:
                for settlement in player.availableSettlements(state):
                    builtSettlement = copy.deepcopy(state)
                    builtSettlement.settlements.append(settlement.getSettlementWithOwner(player.playerId))
                    builtSettlement.getPlayerByIndex(builtSettlement.turn.currentPlayer).resources[ResourceType.BRICK] -= 1
                    builtSettlement.getPlayerByIndex(builtSettlement.turn.currentPlayer).resources[ResourceType.LUMBER] -= 1
                    builtSettlement.getPlayerByIndex(builtSettlement.turn.currentPlayer).resources[ResourceType.WOOL] -= 1
                    builtSettlement.getPlayerByIndex(builtSettlement.turn.currentPlayer).resources[ResourceType.GRAIN] -= 1
                    possibleNextStates.append(builtSettlement)
            stateIndex += 1
                
        #can you build a city?
        stateIndex = 0
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            player = state.getPlayerByIndex(state.turn.currentPlayer)

            if player.resources[ResourceType.GRAIN] >= 2 and \
                        player.resources[ResourceType.ORE] >= 3 and player.numCities(gameState) < 4:
                for settlement in player.settlements(state):
                    if settlement.isCity == False:
                        builtCity = copy.deepcopy(state)
                        next(settlementToUpgrade for settlementToUpgrade in builtCity.settlements if \
                                 settlementToUpgrade == settlement).isCity = True
                        builtCity.getPlayerByIndex(builtCity.turn.currentPlayer).resources[ResourceType.GRAIN] -= 2
                        builtCity.getPlayerByIndex(builtCity.turn.currentPlayer).resources[ResourceType.ORE] -= 3
                        possibleNextStates.append(builtCity)
            stateIndex += 1
            
        return possibleNextStates

    def vp(self, gameState):
        vp = 0
        for settlement in gameState.settlements:
            if settlement.owner == self.playerId:
                vp += 2 if settlement.isCity else 1

        return vp
