from functools import reduce

class Lambda(object):
    def __init__(self, v):
        self.origin = v
        self.values = v
    
    @property
    def list(self):
        return list(self.values)

    @property
    def set(self):
        return set(self.values)

    def reset(self):
        """
        丢弃所有的变换
        """
        self.values = self.origin
        
        return self
    
    def reduce(self, func, initial=None):
        """
        Reduce
 
        :Args:
        - func
        - initial 代替values中的第一个值，作为累计操作的初始值，
        """
        if initial:
            self.values = reduce(func, self.values, initial)
        else:
            self.values = reduce(func, self.values)
        
        return self

    def filter(self, func):
        self.values = filter(func, self.values)
        return self

    def map(self, func):
        self.values = map(func, self.values)
        return self




    