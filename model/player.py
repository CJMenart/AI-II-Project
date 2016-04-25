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

    #determines at what rate you can trade a given resource to the
    #bank; depends on what 'ports' you have.
    #written very shoddily; it was quick this way, and won't run
    #any slower than if I do it using dictionaries
    def bankTradeRate(self, resource, gameState):
        settlements = self.settlements(gameState)
        if resource == ResourceType.WOOL:
            for settlement in settlements:
                spaces = {settlement.adjHex1, \
                          settlement.adjHex2, settlement.adjHex3}
                if Point(1,0) in spaces and Point(1,1) in spaces:
                    #print("Sheep port!")
                    return 2
        if resource == ResourceType.BRICK:
            for settlement in settlements:
                spaces = {settlement.adjHex1, \
                          settlement.adjHex2, settlement.adjHex3}
                if Point(4,1) in spaces and Point(5,1) in spaces:
                    #print("Brick port!")
                    return 2
        if resource == ResourceType.ORE:
            for settlement in settlements:
                spaces = {settlement.adjHex1, \
                          settlement.adjHex2, settlement.adjHex3}
                if Point(0,3) in spaces and Point(-1,4) in spaces:
                    #print("Ore port!")
                    return 2
        if resource == ResourceType.LUMBER:
            for settlement in settlements:
                spaces = {settlement.adjHex1, \
                          settlement.adjHex2, settlement.adjHex3}
                if Point(3,3) in spaces and Point(4,3) in spaces:
                    #print("Wood port!")
                    return 2
        if resource == ResourceType.GRAIN:
            for settlement in settlements:
                spaces = {settlement.adjHex1, \
                          settlement.adjHex2, settlement.adjHex3}
                if Point(1,4) in spaces and Point(0,5) in spaces:
                    #print("Wheat port!")
                    return 2
        
        for settlement in settlements:
            spaces = {settlement.adjHex1, \
                        settlement.adjHex2, settlement.adjHex3}
            if (Point(0,2) in spaces and Point(-1,2) in spaces) \
                or (Point(2,4) in spaces and Point(2,5) in spaces) \
                or (Point(3,0) in spaces and Point(3,-1) in spaces) \
                or (Point(4,0) in spaces and Point(5,-1) in spaces):
                #print ("Misc port!")
                return 3
        return 4

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
    def openSettlementLocations(self, gameState):
        openLocations = []
        for basePoint in pointsOnBoard():
            basePointNbors = basePoint.allAdjacentPoints()
            for point2 in basePointNbors:
                for point3 in [val for val in \
                                basePointNbors if \
                                val in point2.allAdjacentPoints()]:
                    settlement = Settlement(basePoint, point2, point3, -1)
                    #check whether an existing settlement is in the same
                    #space or adjacent
                    legalPlacement = True
                    if settlement in openLocations:
                        legalPlacement = False
                    for existingSettlement in gameState.settlements:
                        if settlement.adjacentOrCloser(existingSettlement):
                            legalPlacement = False
                    if legalPlacement:
                        openLocations.append(settlement)
        #print("num open settlements: ", len(openLocations))
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

    #used for the newest portion of the heuristic
    #not a set of settlements, per se, but of intersections this player has already reached
    def intersections(self, gameState):
        intersects = []
        for r in self.roads(gameState):
            for s in Settlement.adjacentSettlementsByRoad(r):
                if s not in intersects:
                    intersects.append(s)
        return intersects

    #returns the child nodes of a GameState in which this player takes zero or one build options
    def buildSomething(self, gameState):
        possibleNextStates = []

        print('build something')
        
        #the first state represents doing nothing.
        passTurn = copy.deepcopy(gameState)
        passTurn.turn.currentPlayer = passTurn.nextPlayer()
        passTurn.turn.turnState = TurnState.DIE_ROLL
        passTurn.turn.turnNumber += 1
        possibleNextStates.append(passTurn)

        #from there, we create states representing:
        #can you trade resources to the bank to get a resource of your choice?
        #organized by resource--we make all wheat trades, then all brick trades across all
        #states, etc.--so as to avoid redundancies which can become exponentially
        #bothersome in the right situation
        for fromIndex in ResourceType:
            stateIndex = 0
            while stateIndex < len(possibleNextStates):
                state = possibleNextStates[stateIndex]
            
                tradeRate = self.bankTradeRate(fromIndex, gameState)
                if state.getPlayerByIndex(self.playerId).resources[fromIndex] >= tradeRate:
                    #print("Trading ", fromIndex, " at trade rate ", tradeRate)
                    for toIndex in [i for i in ResourceType if i != fromIndex]:
                        traded = copy.deepcopy(state)
                        traded.getPlayerByIndex(self.playerId).resources[fromIndex] -= tradeRate
                        traded.getPlayerByIndex(self.playerId).resources[toIndex] += 1
                        possibleNextStates.append(traded)
                stateIndex += 1

        #from there:
        #can you build a road?
        stateIndex = 0
        print('number of states going into road check: ', len(possibleNextStates))
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            player = state.getPlayerByIndex(self.playerId)
            if player.resources[ResourceType.BRICK] >= 1 and \
                   player.resources[ResourceType.LUMBER] >= 1:
                print("num possible roads: ", len(player.availableRoads(state)))
                for road in player.availableRoads(state):
                    builtRoad = copy.deepcopy(state)
                    # appending road to state
                    builtRoad.roads.append(road.getRoadWithOwner(player.playerId))
                    #print('num roads in state: ', len(builtRoad.roads))
                    builtRoad.getPlayerByIndex(player.playerId).resources[ResourceType.BRICK] -= 1
                    builtRoad.getPlayerByIndex(player.playerId).resources[ResourceType.LUMBER] -= 1
                    # check if creates a longest road if so, update state
                    possLongerLength = self.possibleLongestRoadLength(road, player.roads(builtRoad)) 
                    if possLongerLength >= 5 and \
                            possLongerLength > builtRoad.longestRoadLenWithId[0]: 
                        builtRoad.longestRoadLenWithId = [possLongerLength, player.playerId]
                        print('now player {} has claimed the longest road title with road length of {}'.format(builtRoad.longestRoadLenWithId[1], builtRoad.longestRoadLenWithId[0]) ) 
                    
                    possibleNextStates.append(builtRoad)
            stateIndex += 1

        print('number of states going out of road check: ', len(possibleNextStates))

        #can you build a settlement?
        stateIndex = 0
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            player = state.getPlayerByIndex(self.playerId)

            if player.resources[ResourceType.BRICK] >= 1 and \
                    player.resources[ResourceType.LUMBER] >= 1 and \
                    player.resources[ResourceType.WOOL] >= 1 and \
                    player.resources[ResourceType.GRAIN] >= 1 and player.numBasicSettlements(state) < 5:
                for settlement in player.availableSettlements(state):
                    builtSettlement = copy.deepcopy(state)
                    builtSettlement.settlements.append(settlement.getSettlementWithOwner(player.playerId))
                    builtSettlement.getPlayerByIndex(self.playerId).resources[ResourceType.BRICK] -= 1
                    builtSettlement.getPlayerByIndex(self.playerId).resources[ResourceType.LUMBER] -= 1
                    builtSettlement.getPlayerByIndex(self.playerId).resources[ResourceType.WOOL] -= 1
                    builtSettlement.getPlayerByIndex(self.playerId).resources[ResourceType.GRAIN] -= 1
                    possibleNextStates.append(builtSettlement)
            stateIndex += 1
                
        #can you build a city?
        stateIndex = 0
        while stateIndex < len(possibleNextStates):
            state = possibleNextStates[stateIndex]
            player = state.getPlayerByIndex(self.playerId)

            if player.resources[ResourceType.GRAIN] >= 2 and \
                        player.resources[ResourceType.ORE] >= 3 and player.numCities(state) < 4:
                for settlement in player.settlements(state):
                    if settlement.isCity == False:
                        builtCity = copy.deepcopy(state)
                        print('Built City')
                        next(settlementToUpgrade for settlementToUpgrade in builtCity.settlements if \
                                 settlementToUpgrade == settlement).isCity = True
                        builtCity.getPlayerByIndex(self.playerId).resources[ResourceType.GRAIN] -= 2
                        builtCity.getPlayerByIndex(self.playerId).resources[ResourceType.ORE] -= 3
                        possibleNextStates.append(builtCity)
            stateIndex += 1
            
        return possibleNextStates

    def vp(self, gameState):
        vp = 0
        for settlement in gameState.settlements:
            if settlement.owner == self.playerId:
                vp += 2 if settlement.isCity else 1
        # if have longest road title, add 2 pts
        if gameState.longestRoadLenWithId[1] == self.playerId: 
            vp += 2

        return vp

    # depth first search from the adding road with the direction(settlement) 
    # search down the tree on existing road, note that adding road is not 
    # in existing road. 
    def DFS(self, addingRoad, existingRoad, direction): 
        adjRoads = [r for r in direction.adjacentRoads() if r != addingRoad]
        adjExistingRoads = [r for r in adjRoads if r in existingRoad]
        # recursive step
        if (len(adjExistingRoads) > 0): 
            possibleResult = []
            for rd in adjExistingRoads:
                setDir = next(s for s in Settlement.adjacentSettlementsByRoad(rd) if addingRoad not in s.adjacentRoads())
                #for s in Settlement.adjacentSettlementsByRoad(rd): 
                #    if addingRoad not in s.adjacentRoads(): 
                #        setDir = s 
                DFSresult = self.DFS(rd, [r for r in existingRoad if r != rd], setDir)
                DFSresult[1].append(rd)
                possibleResult.append(DFSresult)
            possibleResult.sort(key = lambda x: -x[0])
            longerPath = possibleResult[0]
            return [longerPath[0]+1, longerPath[1] ] 
        # base case
        else:
            return [0, []]

    # to be called before the adding Roads is inserted into the player's road 
    # list. use the adding Road with -1 owner id. 
    # return int (the possible longest road lenth with the adding road)
    def possibleLongestRoadLength(self, addingRoad, existingRoads): 
        # look at one direction from addingRoad, then the other direction 
        # then sum the roads to get total length
        adjSets =Settlement.adjacentSettlementsByRoad(addingRoad) 
        p1 = self.DFS(addingRoad, existingRoads, adjSets[0])
        # need to take out roads that are already used in one direction 
        p2 = self.DFS(addingRoad, [item for item in existingRoads \
                                       if item not in p1[1]], adjSets[1])
        return 1 + p1[0] + p2[0]
            
