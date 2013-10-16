#import abc
from implementation.Parameters import Parameters

class StatsMonitor(object):

    def __init__(self, agent_class):
        self._agent_class = agent_class

    def getAgentClass(self):
        return self._agent_class

    #__metaclass__ = abc.ABCMeta
    
    '''Returns list of parameters names, which this monitor has to monitor'''
    #@abc.abstractmethod      
    def getParametersNames(self):
        pass

    
    '''Prints aggregated value from stats collected from beginning of simulation'''
    #@abc.abstractmethod
    def printAgregatedValue(self):
        pass
    
    '''Print stats from current simulation step.'''
    '''This method is called in addStats if Parameters.printStats is True'''
    #@abc.abstractmethod
    def printStats(self, stats):
        pass
    
    #@abc.abstractmethod
    def actualStats(self, stats):
        pass
        
