#ShuffleBag code copped from
#http://seanmonstar.com/post/708989796/a-less-random-generator

import random
class ShuffleBag(object):
    def __init__(self, values):
        self.values = values
        self.list = None
    def next(self):
        if (self.list is None) or (len(self.list) == 0):
            self.shuffle()
        return self.list.pop()
    def shuffle(self):
        self.list = self.values[:]
        random.shuffle(self.list)
