#copped from an excellent article at
#http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/

import random

#choose an integer with weighted randomness. The weight of
#each integer is the weight at each index (and thus your selection will
#be from zero to len(weights)
def weighted_choice(weights):
    
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
