from action.Action import Action

class KillAgentAction(Action):
    
    def __init__(self, agent, simLogic):
        self._agent = agent
        self._env = agent.getEnv()
        self._oldCoords = self._env.getAgentPos(agent)
        self._simLogic = simLogic
        self._killed = False
        self._dieAge = self._agent.getCreationTime()
        
    def doAction(self):
        if self._agent.hasToBeKilled():
            self._agent.killAgent()
            self._killed = True
            self._changeAddittionalInfo(1)
            val = self._agent.getParent().getAddittionalInfo("dieAge")
            if val is None:
                val = []
            val.append(self._dieAge)
            self._agent.getParent().setAddittionalInfo("dieAge", val)
            
            
    def rollback(self, index):
        if self._killed:    
            self._agent.rollbackKill()
            self._env.putAgents(self._agent)
            self._env.moveAgent(self._agent, self._oldCoords)
            self._changeAddittionalInfo(-1)
            val = self._agent.getParent().getAddittionalInfo("dieAge")
            val = []
            val.remove(self._dieAge)
            self._agent.getParent().setAddittionalInfo("dieAge", val)
            
    def _changeAddittionalInfo(self, value):
        val = self._agent.getParent().getAddittionalInfo("kill")
        if val is None:
            val = 0
        val += value
        self._agent.getParent().setAddittionalInfo("kill", val)