from multiprocessing import Pool
from functools import partial

def f(x, y):
    return x * y

def superPowerTurboForceGo():
    pool = Pool(5)
    array = [1,2,3,4]
    ys = [5,5,5,5]
    tuples = [(1,5),(2,5),(3,5),(4,5)]
    print (pool.map(partial(f, y=5), array)) 
