#tools for running non-interactive simulation of a game, first for testing and
#later, hopefully, for heuristic-training purposes

from hmin import *
import random

def simulateTurn(gameState):
    if (gameState.turn.turnState == TurnState.DIE_ROLL):
        return simulateDieRoll(gameState)
    else:
        return simulateDecision(gameState)


def simulateDieRoll(gameState):
    states = gameState.getPossibleNextStates()
    roll = random.randint(1,6) + random.randint(1,6)
    if roll == 2:
        return states[0]
    elif roll == 3:
        return states[1]
    elif roll == 4:
        return states[2]
    elif roll == 5:
        return states[3]
    elif roll == 6:
        return states[4]
    elif roll == 8:
        return states[5]
    elif roll == 9:
        return states[6]
    elif roll == 10:
        return states[7]
    elif roll == 11:
        return states[8]
    elif roll == 12:
        return states[9]
    elif roll == 7:
        return states[10]
    else:
        return -1 #error

def simulateDecision(gameState):
    return IHM(gameState, 2)[1]

def skipToGoodPart():
    game = newGame()
    game = game.getPossibleNextStates()[6]
    game = game.getPossibleNextStates()[8]
    game = game.getPossibleNextStates()[10]
    game = game.getPossibleNextStates()[12]
    game = game.getPossibleNextStates()[14]
    game = game.getPossibleNextStates()[16]
    for player in game.players:
        player.resources[ResourceType.WOOL] = 5
        player.resources[ResourceType.BRICK] = 5
        player.resources[ResourceType.ORE] = 5
        player.resources[ResourceType.LUMBER] = 5
        player.resources[ResourceType.GRAIN] = 5
    return game

def simulateQuickGame():
    game = skipToGoodPart()
    while max(game.players[0].vp(game), game.players[1].vp(game), \
              game.players[2].vp(game)) < 10:
        game = simulateTurn(game)
        print("Points: ", game.players[0].vp(game), \
              game.players[1].vp(game), game.players[2].vp(game))
    print("Game Won!")
    print("Points: ", game.players[0].vp(game), \
              game.players[1].vp(game), game.players[2].vp(game))
