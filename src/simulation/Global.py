'''
Created on 2012-05-06

@author: Bogusia
'''

class _Global(object):

    def __init__(self):
        # just for the sake of information
        self.instance = "Instance at %d" % self.__hash__()
        self._count=0
    
    def nextStep(self):
        self._count+=1
    
    def getStep(self):
        return self._count


_global = _Global()

def Global(): return _global