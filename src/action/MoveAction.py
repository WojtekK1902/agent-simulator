from action.Action import Action
from random import Random

class MoveAction(Action):
    
    def __init__(self, agent):
        self._agent = agent
        self._env = agent.getEnv()
        self._oldCoords = self._env.getAgentPos(agent)
        
    def doAction(self):
        coords = self._agent.movePossibilities()
        i = len(coords)
        if i == 0:
            return
        rand = Random()
        while i > 0:
            field = coords[rand.randint(0, len(coords) - 1)]
            if self._env.isFree(field):
                self._env.moveAgent(self._agent, field)
                break
            i -= 1
    
    def rollback(self, index):
        self._env.moveAgent(self._agent, self._oldCoords)

