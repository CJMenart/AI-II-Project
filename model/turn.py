class TurnState(Enum):
    DIE_ROLL = 1
    PLAYER_ACTIONS = 2
    INITIAL_PLACEMENT = 3

class Turn:
    def __init__(self, turnState, currentPlayer):
        self.turnState = turnState
        self.currentPlayer = currentPlayer

    def __init__(self, other):
        self.turnState = other.turnState
        self.currentPlayer = other.currentPlayer
