from action import Action

class AddAgentAction(Action):
    
    def __init__(self, parent, agent):
        self._agent = agent
        self._parent = parent
        self._oldEnv = agent.getEnv()
        self._env = parent.getChildrenEnv()
        
    def doAction(self):
        if self._parent is None or self._agent is None or self._agent.getEnergy() <= 0:
            return
        self._env.putAgents(self._agent)
        self._parent.addChildren(self._agent)
        self._agent.setEnv(self._env)
        
    def rollback(self, index):
        self._env.removeAgent(self._agent)
        self._parent.killChildren(self._agent)
        self._agent.setEnv(self._oldEnv)
        