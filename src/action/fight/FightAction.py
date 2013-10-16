from action.Action import Action

class FightAction(Action):

    def __init__(self, agent, otherAgent):
        self._agent = agent
        self._otherAgent = otherAgent
        self._oldEnergy = agent.getEnergy()
        self._oldEnergy2 = otherAgent.getEnergy()
        self._valid = True
        if self._oldEnergy is None or self._oldEnergy2 is None:
            self._valid = False
        
    def doAction(self):
        if self._valid:
            self._agent.fight(self._otherAgent)
            self._changeAddittionalInfo(1)
            #self._otherAgent.fight(self._agent)

    def rollback(self, index):
        if self._valid:
            self._agent.setEnergy(self._oldEnergy)
            self._otherAgent.setEnergy(self._oldEnergy2)
            self._changeAddittionalInfo(-1)
            
    def _changeAddittionalInfo(self, value):
        val = self._agent.getParent().getAddittionalInfo("fight")
        if val is None:
            val = 0
        val += value
        self._agent.getParent().setAddittionalInfo("fight", val)