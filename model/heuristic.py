from GameState import *
from player import *

#Code pertaining to the heuristic function for H-minimax

#uses a default set of weights
def defaultEvaluation(gameState, playerIndex):
    return evaluateByOpponents(gameState, playerIndex, [5, 2, 10, 5, 1.5])


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
#    Victory points, Resource Cards in Hand, Having 8 or more Cards, Buildable Settlement Locations, Income
def heuristic(gameState, playerIndex, weights):
    heuristicVal = 0

    #first thing we account for is score
    vp = gameState.players[playerIndex].vp(gameState)

    if vp == 10:    #victory state. Immediately return maximum possible heuristic value
        return 100


    #then we will count resources.
    #I'm predicting that training will weight this lightly--after all, what really matters is if
    #you have the right resources to build something
    res = gameState.players[playerIndex].resources
    resourceCount = res[ResourceType.ORE] + res[ResourceType.WOOL] + \
            res[ResourceType.LUMBER] + res[ResourceType.GRAIN] + \
            res[ResourceType.BRICK]

    #do you have too many resources? Be careful
    riskOfRobber = 0 if resourceCount >= 8 else 1

    #we can also count the number of settlement-building opportunities we might have
    #gotta get territory!
    numOptions = len(gameState.getPlayerByIndex(playerIndex).\
                         availableSettlements(gameState))
    

    #we will also count player income--counted in terms of 'pips'
    income = 0
    for settlement in gameState.settlements:
        if settlement.owner == playerIndex:
            for adjHex in {settlement.adjHex1, settlement.adjHex2, settlement.adjHex3}:
                if adjHex.isOnBoard():
                    income += gameState.spaces[adjHex.x][adjHex.y].numPips() * (2 if settlement.isCity else 1)

    return (vp*weights[0] + resourceCount*weights[1] + riskOfRobber*weights[2] + numOptions*weights[3] + income*weights[4])/sum(weights)           

