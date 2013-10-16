from environment.Environment import Environment
from random import Random

class Environment2D(Environment):
    
    def __init__(self, id, width, height):
        self._id = id
        self._width = width
        self._height = height
        self._array = [[None] * height for i in xrange(width)]
        self._positions = {}        

    def getId(self):
        return str(self._id)
    
    def putAgents(self, *agents):
        if len(agents) > self._freeFieldsAmount():
            raise RuntimeError("The 2D board is too small.")
        random = Random()
        for agent in agents:
            x = random.randint(0, self._width - 1)
            y = random.randint(0, self._height - 1)
            if not self._array[x][y]:
                self._placeAgent(agent, x, y)
            else:
                poss = [(i, j) for i in xrange(self._width) for j in xrange(self._height)] 
                for x, y in poss:
                    if not self._array[x][y]:
                        self._placeAgent(agent, x, y)
                        break


    def _freeFieldsAmount(self):
        poss = [(i, j) for i in xrange(self._width) for j in xrange(self._height)]
        return sum([(self._array[pos[0]][pos[1]] is None) for pos in poss])
    
    def _placeAgent(self, agent, x, y):
        self._array[x][y] = agent
        self._positions[agent.getId()] = [x, y]

    def getFreeFields(self, agent):
        try:
            coords = self.getAgentPos(agent)
        except IndexError:
            return []
        result = []
        for x in xrange(coords[0] - 1, coords[0] + 2):
            for y in xrange(coords[1] - 1, coords[1] + 2):
                if x < 0 or x >= self._width:
                    continue
                if y < 0 or y >= self._height:
                    continue
                if self._array[x][y] is None:
                    result.append([x, y])
        return result
    
    def getNeighbours(self, agent):
        try:
            coords = self.getAgentPos(agent)
        except IndexError:
            return []
        result = []
        id = agent.getId()
        for x in xrange(coords[0] - 1, coords[0] + 2):
            for y in xrange(coords[1] - 1, coords[1] + 2):
                if x < 0 or x >= self._width:
                    continue
                if y < 0 or y >= self._height:
                    continue
                if self._array[x][y] is not None and self._array[x][y].getId() != id:
                    result.append([self._array[x][y], x, y])
        return result
    
    def getAgents(self, agent):
        agents = []
        id = None
        if agent is not None:
            id = agent.getId()
        for x in xrange(len(self._array)):
            for y in xrange(len(self._array[x])):
                if self._array[x][y] is not None and self._array[x][y].getId() != id:
                    agents.append(self._array[x][y])
        return agents
    
    def getAgentPos(self, agent):
        coords = self._positions.get(agent.getId(), [])
        if not coords:
            raise IndexError("Agent %s does not exist." % (agent.getId()))
        return coords
    
    def isFree(self, pos):
        x, y = pos
        return False if self._array[x][y] else True
    
    def moveAgent(self, agent, pos):
        newX, newY = pos
        oldCoords = self.getAgentPos(agent)
        self._positions[agent.getId()] = [newX, newY]
        self._array[newX][newY] = agent
        self._array[oldCoords[0]][oldCoords[1]] = None
        
    def removeAgent(self, agent):
        try:
            coords=self.getAgentPos(agent)
            self._positions[agent.getId()]=None
            self._array[coords[0]][coords[1]] = None
        except IndexError:
            return
        
