# this file defines player class that packages player associated data 
# and behavior   
from enum import Enum
from resource import *

class Player:
    def __init__(self, inputPlayerId, resources):
        self.playerId = inputPlayerId
        self.resources = resources
        #below: what a basic player with an empty hand looks like
        #self.resources = {ResourceType.WOOL: 0 , ResourceType.BRICK:0, ResourceType.ORE:0, ResourceType.LUMBER:0, ResourceType.GRAIN:0}

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
            if r.playerId == self.playerId:
                playerRoads.append(r)
        return playerRoads

    # get a list of settlements that belong to the player                                        
    def settlements(self, gameState):
        playerSettlements = []
        for s in gameState.settlements:
            if s.playerId == self.playerId:
                playerSettlements.append(s)
        return playerSettlements


    # get a list of available roads that the player could build
    def availableRoads(self, gameState):
        buildableRoads = []
        for road in openRoadLocations(gameState):
            #Now we need to check if you have another road
            #adjacent to this one
            for existingRoad in self.roads():
                if basePoint == existingRoad.adjHex1:
                    if HexAdjacent(point2, existingRoad.adjHex2):
                        buildableRoads.append(road)
                if basePoint == existingRoad.adjHex2:
                    if HexAdjacent(point2, existingRoad.adjHex1):
                        buildableRoads.append(road)
        return buildableRoads
    
    # get a list of available settlements that the player could build
    def availableSettlements(self, gameState):
        buildableSettlements = []
        for settlement in openSettlementLocations(gameState):
            for road in self.roads(gameState):
                if road.adjHex1 in {basePoint, point2, point3} and \
                        road.adjHex2 in {basePoint, point2, point3}:
                    buildableSettlements.append(settlement)
                    break
        return buildableSettlements
                    

    # build a road that belongs to the player, update gameState
    def buildRoad(self, hex1, hex2, gameState):
        return None

    # build a settlement that belongs to the player, update gameState
