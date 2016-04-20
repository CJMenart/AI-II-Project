from GameState import *
from heuristic import *
import time
from multiprocessing import Pool
from functools import partial

#iterative-deepening H-Minimax
#iteratively does H-Minimax at increasing depth until it starts
#taking longer than the 'time limit', expressed in seconds
#so 'time limit' is not really a time limit right now
def IHM(gameState, timeLimit):
    newState = -1
    hVal = -1

    for depth in range(1,20):
        print("Depth: ", depth)
        timestamp = time.time()
        (hVal, newState) = hMinByDecision(gameState, depth)
        print("Returned from hMinOld.")
        if (time.time() - timestamp >= timeLimit):
            return(hVal, newState)

    return (hVal, newState)

#does H-Minimax with alpha-beta pruning, optimizing to a given depth IN TURNS
#returns (heuristic value for this state based on search, preferred next state)
def hMinByTurn (gameState, targetTurn, multithread = True):
    #print("Starting hMin function.")
    #print("targetTurn: ", targetTurn, ", gameTurn: ", gameState.turn.turnNumber)

    if gameState.turn.turnNumber == targetTurn: #base case
        return (defaultEvaluation(gameState),gameState)

    nextStates = gameState.getPossibleNextStates()
    values = []

    print("len states: ", len(nextStates))

    if multithread:
        pool = Pool(len(nextStates))
        hTuples = pool.map(partial(hMinByTurn, targetTurn = targetTurn, \
                            multithread=False), nextStates)
        for tup in hTuples:
            values.append(tup[0])
        pool.close()
    else:
        for state in nextStates:
            values.append(hMinByTurn(state, targetTurn, False)[0])
   
    #print("Close to ending hMin function.")

    #if this is a chance node, we must do things differently
    if gameState.turn.turnState == TurnState.DIE_ROLL:
        #weighted average of heuristic values based on the dice probabilities
        value = values[0]*1/36 + \
                values[1]*2/36 + \
                values[2]*3/36 + \
                values[3]*4/36 + \
                values[4]*5/36 + \
                values[5]*5/36 + \
                values[6]*4/36 + \
                values[7]*3/36 + \
                values[8]*2/36 + \
                values[9]*1/36 + \
                values[10]*6/36
        # TODO Is this better?:
        # weights = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 6]
        # value = sum(p*q for p,q in zip(values, weights))/36
        return (value, -1)
    else:
        bestChoiceInd = values.index(max(values))
        return(values[bestChoiceInd], nextStates[bestChoiceInd])


#does H-Minimax with alpha-beta pruning, optimizing to the given depth
#returns (heuristic value for this state based on search, preferred next state)
def hMinByDecision (gameState, depth, multithread = True):
    #print("Starting hMin function.")

    nextStates = gameState.getPossibleNextStates()
    values = []

    print("Len nextStates: ",len(nextStates))

    if depth == 1 and multithread:
        stateInd = 0
        poolSize = 50
        pool = Pool(poolSize)
        while (stateInd < len(nextStates)):
            
        #for state in nextStates:
            print("About to pool.")

            nextVals = pool.map(defaultEvaluation, nextStates[stateInd:min(\
                            len(nextStates), stateInd+poolSize)])
            values.extend(nextVals)
            stateInd += poolSize
        pool.close()
    elif depth == 1 and not multithread:
        for state in nextStates:
            values.append(defaultEvaluation(state))
        
    elif depth > 1 and multithread:
        pool = Pool(len(nextStates))
        hTuples = pool.map(partial(hMinByDecision, depth = depth-1, \
                            multithread=False), nextStates)
        for tup in hTuples:
            values.append(tup[0])
        pool.close()
    elif depth > 1 and not multithread:
        for state in nextStates:
            values.append(hMinByDecision(state, depth-1, False)[0])
    else:
        return -1 #error. Depth must be at least 1

    #print("Close to ending hMin function.")

    #if this is a chance node, we must do things differently
    if gameState.turn.turnState == TurnState.DIE_ROLL:
        #weighted average of heuristic values based on the dice probabilities
        value = values[0]*1/36 + \
                values[1]*2/36 + \
                values[2]*3/36 + \
                values[3]*4/36 + \
                values[4]*5/36 + \
                values[5]*5/36 + \
                values[6]*4/36 + \
                values[7]*3/36 + \
                values[8]*2/36 + \
                values[9]*1/36 + \
                values[10]*6/36
        # TODO Is this better?:
        # weights = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 6]
        # value = sum(p*q for p,q in zip(values, weights))/36
        return (value, -1)
    else:
        bestChoiceInd = values.index(max(values))
        return(values[bestChoiceInd], nextStates[bestChoiceInd])
