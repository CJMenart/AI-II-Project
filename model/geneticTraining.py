from hmin import *
from weighted_random import *
import random
from simulation import simulateTurn

#takes a population, or vector, of weights vectors for
#Catan agents, and returns a vector of same--but a better one--
#with the last best-known vector on top of the list
def generation(population):
    #this vector will keep track of our fitness ratings
    scores = [0]*len(population)

    #every agent will play in up to this many games
    trialsLeft = 3

    matchupsBag = ShuffleBag(range(1,len(population)))

    while trialsLeft > 0:
        
        playerIndices = [matchupsBag.next(), matchupsBag.next(), \
                   matchupsBag.next()]
        
        (scores[playerIndices[0]],scores[playerIndices[1]],\
                scores[playerIndices[2]]) = \
                playGame(population[playerIndices[0]],\
                population[playerIndices[1]],population[playerIndices[2]])

        if len(matchupsBag.values) < 3:
            trialsLeft -= 1

    #now create new population based on scores
    #best individual automatically gets a pass
    newPopulation = population[scores.index(max(scores))]
    weightVectorLen = len(population[0])
    
    while len(newPopulation) < len(population):
        parentA = population[weighted_random(scores)]
        parentB = population[weighted_random(scores)]
        crossPoint = random.randrange(weightVectorLen)
        child = [parentA[0:crossPoint]].\
                             extend(parentB[crossPoint:weightVectorLen])
        while random.randrange(2) == 0:
            toMutate = random.range(weightVectorLen)
            child[toMutate] = max(0, child[toMutate] + random.gauss(0, 0.5))

        newPopulation.append(child)

    print("Generation Complete:")
    for child in newPopulation:
        print(child)

    return newPopulation

def playGame(player1Weights, player2Weights, player3Weights):

    maxTurns = 50
    weights = [player1Weights, player2Weights, player3Weights]

    game = newGame()


    vps = [p.vp(game) for p in game.players]
    while max(vps) < 10 and game.turn.turnNumber < maxTurns: #game.players[0].vp(game), game.players[1].vp(game), game.players[2].vp(game)) < 10:
        game = simulateTurn(game, weights[game.turn.currentPlayer])
        vps = [p.vp(game) for p in game.players]
        print("Turn ", game.turn.turnNumber, " ,", game.turn.turnState)
        print("Points: ", vps) #game.players[0].vp(game), \
        #game.players[1].vp(game), game.players[2].vp(game))
    print("Game Done!")
    print("Points: ", vps) #game.players[0].vp(game), \

    if max(vps) < 10:
        return (vps[0]/2,vps[1]/2,vps[2]/2)
    else:
        return (vps[0],vps[1],vps[2])
