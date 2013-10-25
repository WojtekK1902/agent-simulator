from action.ActionManager import ActionManager
from environment.AddressManager import AddressManager
from implementation.Parameters import Parameters

class SimLogic(object):
    
    timestamp = 0
    
    def __init__(self):
        self._actionManager = ActionManager()
        self._addressManager = AddressManager()
        self._agents = []
        self._visualisationListeners = {}
        self._stepsMonitor = None
        self._actionsListener = None

    def doStep(self):
        try:
            self._actionManager.clear()
            self._decisionPhase()
            self._executivePhase()
            self._visualise()
            self._setStats()
            if self._actionsListener is not None:
                self._actionsListener.actionStats(self._actionManager.getMeetingActionStats())
                
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    def runSimulation(self, simSteps):        
        raise NotImplementedError()

    def decisionPhase(self):
        raise NotImplementedError()
    
    def executivePhase(self):
        raise NotImplementedError()
    
    def visualise(self):
        raise NotImplementedError()

    def setAgentStepsMonitor(self, stepsMonitor):
        self._stepsMonitor = stepsMonitor
    
    def addVisualisationListener(self, listener, agentClass):
        '''Listener have to have visualise(param) method'''
        list = self._visualisationListeners.get(agentClass, []) 
        list.append(listener)
        self._visualisationListeners[agentClass] = list
         
    def setStatsListener(self, listener):
        '''Listener have to have stats(param) method'''
        self._statsListener = listener
        
    def setActionsListener(self, listener):
        self._actionsListener = listener
        
    def addAgents(self, *agents):
        for agent in agents:
            agent.getEnv().putAgents(agent)
            self._agents += [agent]
        
    def addFlatAgents(self, agentClass, agentCount, agentEnv):
        '''TODO - needs implementation.
        If we want to simplify creating flat structure of agents
        this method used in initialization can be usefull.'''
        pass
        
    def _createAgent(self, agentClass, env):
        '''TODO - will be used with addFlatAgents.'''
        agent = agentClass(self._addressManager.getNextAddress(), env)
        return agent

    def killAgent(self, agent):
        env = agent.getEnv()
        env.removeAgent(agent)
        self._agents.remove(agent)
        
    def _setStats(self):
        statsData = {}
        for rootAgent in self._agents:
            for agent in rootAgent.getDescendants(parent=True):
                list = statsData.get(agent.__class__, [])
                agentAttr = []
                for method in self._statsListener.getGetters(agent.__class__):
                    agentAttr.append(getattr(agent, method)())

                list.append(agentAttr)
                statsData[agent.__class__] = list

        for key in statsData.keys():
            data = statsData.get(key, [])
            self._statsListener.stats(data, key)