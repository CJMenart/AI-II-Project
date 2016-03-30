from GameState import *
from player import *

#Code pertaining to the heuristic function for H-minimax


#the evaluation fed to H-Mnimax
def evaluate(gameState, playerIndex):
    myScore = heuristic(gameState, playerIndex)

    opponentScores = []

    for opponentIndex in [i for i in range(0,len(gameState.players)) if i != playerIndex]:
        opponentScores.append(heuristic(gameState, opponentIndex))

    return myScore / (max(opponentScores)/2 + (sum(opponentScores)/len(opponentScores))/2)



#evaluates a 'score' for how close a given player is to victory
def heuristic(gameState, playerIndex):
    heuristicVal = 0

    #first thing we should account for is score
    vp = 0
    for settlement in gameState.settlements:
        if settlement.owner == playerIndex:
            vp += 2 if settlement.isCity else 1

    if vp == 10:    #victory state. Return maximum possible heuristic value
        return 100

    vpVal = vp*10

    #Right now, there's no score apart from settlements.
    #So we'll just give VP a large weight and not count settlments
    #separately, for now

    #but we will count resources
    res = gameState.players[playerIndex].resources
    resourceCount = res[ResourceType.ORE] + res[ResourceType.WOOL] + \
            res[ResourceType.LUMBER] + res[ResourceType.GRAIN] + \
            res[ResourceType.BRICK]
    resourceVal = -1
    if resourceCount < 8:
        resourceVal = resourceCount / 7 * 100
    else:
        resourceVal = 50

    #we can also count the number of build opportunities we might have
    numOptions = len(gameState.players[playerIndex].\
                         availableSettlements(gameState))
    optionVal = -1
    if numOptions < 10:
        optionVal = numOptions / 10 * 100
    else:
        optionVal = 100

    print(vpVal, resourceVal, optionVal)
    return vpVal*2/3 + resourceVal/6 + optionVal/6            

