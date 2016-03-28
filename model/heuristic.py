from GameState import *
from player import *

#Code pertaining to the heuristic function for H-minimax

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
    resourceCount = sum(gameState.players[playerIndex].resources)
    resourceVal = -1
    if resourceCount < 8:
        resourceVal = resourceVal / 7 * 100
    else:
        resourceVal = 50

    #we can also count the number of build opportunities we might have
    numOptions = len(gameState.players[playerIndex].\
                         availableSettlementLocations(gameState))
    optionVal = -1
    if numOptions < 10:
        optionVal = numOptions / 10 * 100
    else:
        optionVal = 100

    return vpVal*2/3 + resourceVal/6 + optionVal/6            
