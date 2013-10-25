class MonitorsHolder(object):

    def __init__(self):
        self._monitors = {}
        self._parametersNames = {}
        self._getters = {}
        
    def registerMonitor(self, monitor):
        monitors = self._monitors.get(monitor.getAgentClass(), [])
        monitors.append(monitor)
        self._monitors[monitor.getAgentClass()] = monitors

    '''Collects stats in each simulation step'''        
    def stats(self, params, agentClass):
        if self._monitors.get(agentClass, None) is None:
            return
        stats = {}
        names = self._getParametersNames(agentClass)

        for i in xrange(len(names)):
            onlyOneParams = []
            for param in params:
                onlyOneParams.append(param[i])
            stats[names[i]] = onlyOneParams
        for monitor in self._monitors[agentClass]:
            monitor.actualStats(stats)
            
    '''Returns all parameters names from all monitors, which monitor agentClass'''
    def _getParametersNames(self, agentClass):
        if self._parametersNames.get(agentClass, None) is not None:
            return self._parametersNames.get(agentClass)
        result = []
        
        if self._monitors.get(agentClass, None) is None :
            return []
        for monitor in self._monitors[agentClass]:
            paramsNames = monitor.getParametersNames()
            for name in paramsNames:
                if name not in result:
                    result.append(name)
        self._parametersNames[agentClass] = result
        return result
    
    '''Returns getters names (of monitored attributes) from agentClass.'''
    def getGetters(self, agentClass):
        if self._getters.get(agentClass, None) is not None:
            return self._getters[agentClass]
        getters = []
        
        for param in self._getParametersNames(agentClass):
            getters.append("get" + param[0].upper() + param[1:])
        self._getters[agentClass] = getters
        return getters
        
    '''Prints stats values aggregated from begining of simulation'''
    def printAgregatedValues(self):
        for monitors in self._monitors.values():
            for monitor in monitors:
                monitor.printAgregatedValue()


