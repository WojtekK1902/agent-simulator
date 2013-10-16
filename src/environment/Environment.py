#import abc

class Environment(object):
    
    #__metaclass__ = abc.ABCMeta
    
    #@abc.abstractmethod
    def getId(self):
        '''Returns an ID of an environment.'''
        pass
    
    #@abc.abstractmethod
    def putAgents(self, *agents):
        '''Places agent or list of agents in the environment.'''
        pass
    
    #@abc.abstractmethod
    def removeAgent(self, agent):
        '''Removes agent from environment'''
        pass
    
    #@abc.abstractmethod
    def getAgents(self, agent):
        pass
    
    #@abc.abstractmethod
    def getFreeFields(self, agent):
        '''Returns free fields in the neighbourhood of an agent.'''
        pass

    #@abc.abstractmethod
    def getNeighbours(self, agent):
        '''Returns neighbours of an agent.'''
        pass
    
    #@abc.abstractmethod
    def getAgentPos(self, agent):
        '''Returns position of an agent in the environment.'''
        pass

    #@abc.abstractmethod
    def isFree(self, pos):
        '''Checks whether position pos is not occupied by an agent.'''
        pass

    #@abc.abstractmethod
    def moveAgent(self, agent, pos):
        '''Moves agent to the position pos.'''
        pass
    
    def putAgent(self, agent, pos):
        self.putAgents(agent)
        self.moveAgent(agent, pos)
    