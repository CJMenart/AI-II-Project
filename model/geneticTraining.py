from hMin import *

#takes a population, or vector, of weights vectors for
#Catan agents, and returns a vector of same--but a better one--
#with the last best-known vector on top of the list
def generation(population):
    #this vector will keep track of our fitness ratings
    scores = [0]*len(population)

    #every agent will play in up to this many games
    trialsLeft = 3

    trialsLeft -= 1
    matchupsBag = ShuffleBag(range(1:len(population)))

    while trialsLeft > 0:
        
        players = [matchupsBag.next(), matchupsBag.next(), \
                   matchupsBag.next()]
        
        
