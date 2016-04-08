#tools for running non-interactive simulation of a game, first for testing and
#later, hopefully, for heuristic-training purposes

from hmin import *
import random

def simulateTurn(gameState):
    if (gameState.turn.turnState == TurnState.DIE_ROLL):
        return simulateDieRoll(gameState)[0]
    else:
        return simulateDecision(gameState)

def simulateTurnExplain(gameState): # returns (new game state, what happened)
    if (gameState.turn.turnState == TurnState.DIE_ROLL):
        return simulateDieRoll(gameState)
    else:
        ts = gameState.turn.turnState
        return (simulateDecision(gameState), ts)

def simulateDieRoll(gameState):
    states = gameState.getPossibleNextStates()
    r1 = random.randint(1,6)
    r2 = random.randint(1,6)
    roll = r1 + r2
    #if roll == 2:
    #    return states[0]
    #elif roll == 3:
    #    return states[1]
    #elif roll == 4:
    #    return states[2]
    #elif roll == 5:
    #    return states[3]
    #elif roll == 6:
    #    return states[4]
    #elif roll == 8:
    #    return states[5]
    #elif roll == 9:
    #    return states[6]
    #elif roll == 10:
    #    return states[7]
    #elif roll == 11:
    #    return states[8]
    #elif roll == 12:
    #    return states[9]
    #elif roll == 7:
    #    return states[10]
    #else:
    #    return -1 #error
    stateIdx = roll - 3 + (6 if roll==7 else (1 if roll < 7 else 0))
    ## TODO: factor a roll-specific version out of gameState.getPossibleNextStates() to not waste time making and modifiying 9 extra gameState copies!
    return (states[stateIdx], (r1, r2))

def simulateDecision(gameState):
    ## HMin functions return both heuristic evals and state. We take [1] because here we
    #only want state.
    print("Calling simulateDecision")
    return hMinByDecision(gameState, 1, False)[1]

def skipToGoodPart(**kwargs):
    game = newGame(**kwargs)
    ## States here are arbitrary, to get past the portion of the game that thus far
    #  is still prohibitively slow
    game = game.getPossibleNextStates()[13]
    game = game.getPossibleNextStates()[16]
    game = game.getPossibleNextStates()[29]
    game = game.getPossibleNextStates()[42]
    game = game.getPossibleNextStates()[55]
    game = game.getPossibleNextStates()[68]
    for player in game.players:
        #print player.resources
        for resource in ResourceType:
            player.resources[resource] += 2
        assert player.resources[ResourceType.WOOL] >= 2
        #player.resources[ResourceType.WOOL] = 5
        #player.resources[ResourceType.BRICK] = 5
        #player.resources[ResourceType.ORE] = 5
        #player.resources[ResourceType.LUMBER] = 5
        #player.resources[ResourceType.GRAIN] = 5
    return game

def simulateQuickGame():
    game = skipToGoodPart()
    # If vp were a method of GameState rather than player, could do:
    # vps = map(game.vp, game.players)
    vps = [p.vp(game) for p in game.players]
    while max(vps) < 10: #game.players[0].vp(game), game.players[1].vp(game), game.players[2].vp(game)) < 10:
        game = simulateTurnExplain(game)[0]
        vps = [p.vp(game) for p in game.players]
        print("Turn ", game.turn.turnNumber, " ,", game.turn.turnState)
        #print("Points: ", vps) #game.players[0].vp(game), \
        #      game.players[1].vp(game), game.players[2].vp(game))
    print("Game Won!")
    print("Points: ", vps) #game.players[0].vp(game), \
    #          game.players[1].vp(game), game.players[2].vp(game))

if __name__ == "__main__":
    simulateQuickGame()
