from action.Action import Action

class RemoveAgentAction(Action):
    
    def __init__(self, parent, agent):
        self._agent = agent
        self._parent = parent
        self._env = agent.getEnv()
        self._oldCoords = self._env.getAgentPos(agent)
        
    def doAction(self):
        if self._parent is None or self._agent is None or self._agent.getEnergy() <= 0:
            return
        self._env.removeAgent(self._agent)
        self._parent.killChildren(self._agent)
    
    def rollback(self, index):
        self._env.putAgent(self._agent, self._oldCoords)
        self._parent.addChildren(self._agent)
        self._agent.setEnv(self._env)

