class TurnState(Enum):
    DIE_ROLL = 1
    PLAYER_ACTIONS = 2
    INITIAL_PLACEMENT = 3

class Turn:
    def __init__(self, turnState, currentPlayer):
        self.turnState = turnState
        self.currentPlayer = currentPlayer
