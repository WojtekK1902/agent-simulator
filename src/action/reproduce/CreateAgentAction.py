from action.Action import Action
from numpy import mean

class CreateAgentAction(Action):

    def __init__(self, agent1, agent2, simLogic):
        self._agent1 = agent1
        self._agent2 = agent2
        self._simLogic = simLogic
        self._createdAgent = None
    
    def doAction(self):
        gen1 = self._agent1.getGenotype()
        gen2 = self._agent2.getGenotype()
        self._createdAgent = self._agent1.getParent().addAgent(self._agent1.__class__, self._agent1.getEnv())
        energy1 = self._agent1.getEnergy()
        energy2 = self._agent2.getEnergy()
        parentsFightsWon = mean([self._agent1.getWonFightsCount(), self._agent2.getWonFightsCount()])
        parentsFightsLost = mean([self._agent1.getLostFightsCount(), self._agent2.getLostFightsCount()])
        #print parentsFightsWon, parentsFightsLost
        self._createdAgent.setNewGenotype(gen1, gen2, energy1, energy2, parentsFightsWon, parentsFightsLost)
        self._changeAddittionalInfo(1)
        
    def rollback(self, index):
        if not self._createdAgent is None:
            self._createdAgent.killAgent()
            self._changeAddittionalInfo(-1)
            
    def _changeAddittionalInfo(self, value):
        val = self._agent1.getParent().getAddittionalInfo("reproduce")
        if val is None:
            val = 0
        val += value
        self._agent1.getParent().setAddittionalInfo("reproduce", val)