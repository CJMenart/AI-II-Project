from GameState import *
from player import *

#Code pertaining to the heuristic function for H-minimax

#uses a default set of weights
def defaultEvaluation(gameState, playerInd, weights = -1):
    if weights == -1: #default heuristic
        weights = [9,1,8,0.4,2,0.5]
    #return evaluateByOpponents(gameState, playerInd, [6, 1, 8, 0.4, 1.5, 1.5])
    return heuristic(gameState, playerInd, weights)

#the evaluation fed to H-Mnimax
def evaluateByOpponents(gameState, playerIndex, weights):
    myScore = heuristic(gameState, playerIndex, weights)

    opponentScores = []

    #we count scores of 0 as 0.25 to avoid divide-by-0 errors. Usually it won't matter.
    #no one has a score of zero after the first round
    for opponentIndex in [i for i in range(0,len(gameState.players)) if i != playerIndex]:
        opponentScores.append(max(heuristic(gameState, opponentIndex, weights),0.25))

    return myScore / (max(opponentScores)/2 + (sum(opponentScores)/len(opponentScores))/2)


#evaluates a 'score' for how close a given player is to victory
#'Weights' is a vector of coefficients to be used for the weighted averages
#of the following:
#    Victory points, Resource Cards in Hand, Having 8 or more Cards,
#    Quality of Opportunities for Expansion, Income, Having the Resources to Build Things
def heuristic(gameState, playerIndex, weights):

    heuristicVal = 0
    player = gameState.getPlayerByIndex(playerIndex)

    #first thing we account for is score
    vp = player.vp(gameState)

    if vp == 10:    #victory state. Immediately return maximum possible heuristic value
        return 100


    #then we will count resources.
    #I'm predicting that training will weight this lightly--after all, what really matters is if
    #you have the right resources to build something
    resourceCount = player.numCards()
    
    #do you have too many resources? Be careful
    riskOfRobber = 0 if resourceCount >= 8 else 1

    #OLD VERSION:
    #we can also count the number of settlement-building opportunities we might have
    #gotta get territory!
    #numOptions = len(gameState.getPlayerByIndex(playerIndex).\
    #                     availableSettlements(gameState))

    #NEW VERSION: Account for the quality of each building site left on the board
    #and their distance from the player

    #print("Starting to evaluate expansion opportunity")

    expansionOpportunity = 0

    takenByOpponents = set([])

    for opponent in [val for val in gameState.players if val.playerId != playerIndex]:
        takenByOpponents = takenByOpponents.union(set(opponent.availableSettlements(gameState)))
    
    openSettlements = list(set(player.openSettlementLocations(gameState)).difference(takenByOpponents))
    intersections = player.intersections(gameState)

    #print("Num of locations to examine: ", len(openSettlements))
    
    distances = [11]*len(openSettlements) #correspondance by index with openSettlements

    #here's where it gets n-squared
    for intersection in intersections:
        for sInd in range(0,len(openSettlements)):
            settlement = openSettlements[sInd]
            xI = sum([intersection.adjHex1.x, intersection.adjHex2.x, intersection.adjHex3.x])/3
            yI = sum([intersection.adjHex1.y, intersection.adjHex2.y, intersection.adjHex3.y])/3
            xS = sum([settlement.adjHex1.x, settlement.adjHex2.x, settlement.adjHex3.x])/3
            yS = sum([settlement.adjHex1.y, settlement.adjHex2.y, settlement.adjHex3.y])/3
            distanceInRoads = round(abs(xI-xS) + abs(xI+yI-xS-yS) + abs(yI-yS))
            distances[sInd] = min(distances[sInd], distanceInRoads)

    #now assign value 
    for sInd in range(0,len(openSettlements)):
        settlement = openSettlements[sInd]
        expansionOpportunity = expansionOpportunity + \
                        settlement.levelOfIncome(gameState)/(distances[sInd]+1)

    #print("expansionOpp: ", expansionOpportunity)

    #we will also count player income--counted in terms of 'pips'
    income = 0
    for settlement in gameState.settlements:
        if settlement.owner == playerIndex:
            income += settlement.levelOfIncome(gameState)

    #Okay, this one is a bit less obvious than the others. I'm adding it later on,
    #because I've observed that in the absence of trading, it's difficult to save
    #up for the important things. So this places value on doing said saving
    res = gameState.getPlayerByIndex(playerIndex).resources
    savings = min(res[ResourceType.BRICK], 1) + min(res[ResourceType.WOOL], 1) + \
                min(res[ResourceType.LUMBER], 1) + min(res[ResourceType.ORE], 3) + \
                min(res[ResourceType.GRAIN], 2)

    return (vp*weights[0] + resourceCount*weights[1] + riskOfRobber*weights[2] + expansionOpportunity*weights[3] + \
                income*weights[4] + savings*weights[5])           

