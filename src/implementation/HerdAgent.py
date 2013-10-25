from agent.Agent import Agent
from environment.Environment2D import Environment2D
from environment.AddressManager import AddressManager
from implementation.Specimen import Specimen
from simulation.SimLogic import SimLogic
from random import Random

class HerdAgent(Agent):
    
    visualise = ['count', 'energy', 'min', 'max'] #'reproduceCount', 'dieCount']
    stats = ['meetings','fights','reproduceCount','age','genotypes','dieAge']
    
    def __init__(self, env, childrenEnv=None):
        addr = AddressManager.getAddress(None)
        Agent.__init__(self, addr, env, childrenEnv)
        self._reprCount = 0
        self._rand = Random()
        self._reproductionSuccessHistory = [] #list of booleans - True=reproduction succeeded
        self._mutationDistance = 1.0 #used in adaptive mutation
           
    def getCount(self):
        return len(self.getChildren()) 
        
    def addAgents(self, *agents):
        for agent in agents:
            childAddr = AddressManager.getAddress(self)
            agent.setId(childAddr)
            self.getChildrenEnv().putAgents(agent)
            self.addChildren(agent)
        
    def addAgent(self, agentClass, agentEnv):
        childAddr = AddressManager.getAddress(self)
        child = agentClass(childAddr, self.getChildrenEnv())
        self.getChildrenEnv().putAgents(child)
        self.addChildren(child)
        return child

    def getPos(self):
        return self.getEnv().getAgentPos(self)    

    def getEnergy(self):
        result = 0.0
        for child in self.getChildren():
            result += child._energy
        return result

    def getEnergies(self):
        result = []
        for child in self.getChildren():
            result.append(child.getEnergy())
        return result

    def getBestGenotype(self):
        best = None
        for i in range(len(self.getChildren())):
            if best == None or self.getChildren()[i].getFitness() < best:
                best = i
        return self.getChildren()[best].getGenotype()
    
    def getMin(self):
        result = 1000
        for child in self.getChildren():
            if result>child.getFitness():
                result = child.getFitness()
        return result
    
    def getMax(self):
        result = 0
        for child in self.getChildren():
            if result<child.getFitness():
                result = child.getFitness()
        return result

    def getWantReproduceCount(self):
        return sum(1 for child in self.getChildren() if child.wantToReproduce())

    def getReproduceCount(self):
        #result = 0
        #if self._reprCount == 0:
        #    self._reprCount = self._getAdditionalInfo("reproduce")
        #    result = self._reprCount
        #else:
        #    result = self._reprCount
        #    self._reprCount = 0 
        #return result 
        return self._getAdditionalInfo("reproduce")
        
    def getDieCount(self):
        return self._getAdditionalInfo("kill")
        
    def getMeetings(self):
        return self._getAdditionalInfo("meeting")
    
    def getFights(self):
        return self._getAdditionalInfo("fight")
    
    def getAge(self):
        result = []
        for child in self.getChildren():
            result.append(SimLogic.timestamp-child.getCreationTime())
        return result
    
    def getDieAge(self):
        val = self.getAddittionalInfo("dieAge")
        if val is None:
            val = []
        return val    
    
    def getGenotypes(self):
        result = []
        for child in self.getChildren():
            result.append(child.getGenotype())
        return result
    
    def getFitnesses(self):
        result = []
        for child in self.getChildren():
            result.append(child.getFitness())
        return result
    
    def _getAdditionalInfo(self, info):
        val = self.getAddittionalInfo(info)
        if val is None:
            val = 0
        self.setAddittionalInfo(info, 0)
        return val
    
    def getMigrationDestination(self):
        neighbours = self.getEnv().getAgents(self)
        if len(neighbours) == 0:
            return None
        return neighbours[self._rand.randint(0, len(neighbours)-1)]

    def addReproductionSucccess(self):
        self._reproductionSuccessHistory.append(True)

    def addReproductionFail(self):
        self._reproductionSuccessHistory.append(False)

    def getReproductionSuccessHistory(self):
        return self._reproductionSuccessHistory

    def getMutationDistance(self):
        return self._mutationDistance
    
    def setMutationDistance(self, newValue):
        self._mutationDistance = newValue