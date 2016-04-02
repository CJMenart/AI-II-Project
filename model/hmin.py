from GameState import *
from heuristic import *
import time

#iterative-deepening H-Minimax
#iteratively does H-Minimax at increasing depth until it starts
#taking longer than the 'time limit', expressed in seconds
def IHM(gameState, timeLimit):
    newState = -1
    hVal = -1

    for depth in range(1,20):
        print("Depth: ", depth)
        timestamp = time.clock()
        (hVal, newState) = hMin(gameState, depth)
        if (time.clock() - timestamp >= timeLimit):
            return(hVal, newState)

    return (hVal, newState)

#does H-Minimax with alpha-beta pruning, optimizing to the given depth
#returns (heuristic value for this state based on search, preferred next state)
def hMin (gameState, depth):
    nextStates = gameState.getPossibleNextStates()
    values = []

    if depth > 1:
        for state in nextStates:
            values.append(hMin(state, depth-1)[0])
    elif depth == 1:
        for state in nextStates:
            values.append(defaultEvaluation(state, state.turn.currentPlayer))
    else:
        return -1 #error. Depth must be at least 1

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
        return (value, -1)
    else:
        bestChoiceInd = values.index(max(values))
        return(values[bestChoiceInd], nextStates[bestChoiceInd])
