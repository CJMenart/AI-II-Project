class GameState:
    #Tentative data members:
    #spaces: grid keeping track of hex types/numbers
    #players: list of structures with info like hands, color, etc.
    #peices: list of wooden peices like settlements, roads, roobers, with
    #       their positions
    #Turn: info specifying at what point in time of gameplay we're at.
    
    #Two constructors: a copy constructor and one that passes in all data
    #variables individually

    #This one may be unnecessary
    def __init__(self, spaces, players, peices, turn):
        self.spaces = spaces
        self.players = players
        self.peices = peices
        self.turn = turn

    def __init__(self, otherGameState):
        self.spaces = otherGameState.spaces
        self.players = otherGameState.players
        self.peices = otherGameState.peices
        self.turn = otherGameState.turn



#Returns a GameState representing a brand-new game
#also providing example of what member data is supposed to look like
def NewGame():
    
