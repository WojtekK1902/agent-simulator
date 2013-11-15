from simulation.SimLogic import SimLogic
class Agent(object):

    visualise = []
    stats = []

    def __init__(self, id, env=None, childrenEnv=None):
        self._id = id
        self._env = env
        self._childrenEnv = childrenEnv
        self._parent = None
        self._children = []
        self._isDuringMeeting = False
        self._kill = False
        self._creationTime = SimLogic.timestamp
        self._addittionalInfo = {}

    def getId(self):
        return self._id
    
    def setId(self, newId):
        self._id = newId

    def getCreationTime(self):
        return self._creationTime
    
    def getEnv(self):
        return self._env

    def setEnv(self, env):
        self._env = env
        
    def getChildrenEnv(self):
        return self._childrenEnv

    def setChildrenEnv(self, env):
        self._childrenEnv = env

    def getParent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent

    def addChildren(self, *childs):
        for child in childs:
            self._children += [child]
            child.setParent(self)

    def getChildren(self):
        return self._children

    def getDescendants(self, parent=False):
        descendants = [self] if parent else []
        self._descendants(descendants)
        return descendants
    
    def isDuringMeeting(self):
        return self._isDuringMeeting
    
    def setAgentMeeting(self,isDuringMeeting):
        self._isDuringMeeting=isDuringMeeting
    
    def movePossibilities(self):
        return []
    
    def meetAgent(self):
        for neighbour in self.getEnv().getNeighbours(self):
            if neighbour[0].isDuringMeeting() is False:
                return neighbour[0]
        return None
     
    def _descendants(self, gathered=[]):
        for child in self.getChildren():
            gathered += [child]
            child._descendants(gathered)
    
    def killChildren(self, *childs):
        for child in childs:
            for c in self._children:
                if c.getId() == child.getId():  
                    self._children.remove(c)
                    break
                
    def killAgent(self):
        self.getEnv().removeAgent(self)
        if self.getParent() is None:
            print self
            print 'Agent: killAgent - odwolanie do SimLogic, bo to Herd?'
        self.getParent().killChildren(self)
    
    def getFitness(self):
        '''Returns value (float) of function, which domain is genotype'''
        pass

    def wantToReproduce(self):
        '''Returns True if agent want to reproduce, if not there will be fight'''
        return None
    
    def getEnergy(self):
        return None
    
    def setAfterReproductionEnergy(self):
        '''Changes parent energy during reproduction'''
        pass
    
    def rollbackReproductionEnergy(self):
        pass
        
    def getGenotype(self):
        return None
    
    def setNewGenotype(self, gen1, gen2):
        '''Creates new genotype from parents genotypes. There can be some mutations 
        implemented here.'''
        '''gen1, gen2 - genotypes of parent1 and parent2'''
        pass
    
    def fight(self, otherAgent):
        '''Determines how fights are implemented'''
        pass
    
    def wantToMigrate(self):
        '''Returns True if agent wants to migrate''' 
        return None
    
    def getMigrationDestination(self):
        '''Returns agent, which will be migration destination'''
        return None
        
    def kill(self):
        '''This method is called when agent has to die, for example when his energy is 0'''
        self._kill = True
        
    def rollbackKill(self):
        self._kill = False
        
    def hasToBeKilled(self):
        '''This method is called by KillAgentAction to determine if this agent should be killed'''
        return self._kill
    
    def setAddittionalInfo(self, name, value):
        self._addittionalInfo[name] = value
        
    def getAddittionalInfo(self, name):
        return self._addittionalInfo.get(name, None)

    def wantToMeet(self):
        return True

    def __str__(self):
        parent = self._parent.getId() if self._parent else 'None'
        env = self.getEnv().getId() if self._env else 'None'
        childEnv = self.getChildrenEnv().getId() if self._childrenEnv else 'None'
        children = map(lambda x: x.getId(), self.getChildren())
        return 'Agent(%s, env=%s, childEnv=%s, parent=%s, children=%s)' % ( 
            tuple(map(lambda x: str(x), [self.getId(), env, childEnv, parent, children])))

    def __repr__(self):
        return self.__str__()
    
   