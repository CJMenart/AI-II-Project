from enum import Enum

class TurnState(Enum):
    DIE_ROLL = 1
    PLAYER_ACTIONS = 2
    INITIAL_PLACEMENT = 3
    MOVE_ROBBER = 4

class Turn:
    def __init__(self, turnState, currentPlayer, turnNumber):
        self.turnState = turnState
        self.currentPlayer = currentPlayer
        self.turnNumber = turnNumber
        
