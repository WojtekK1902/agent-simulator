
class ActionMonitorsHolder(object):
    
    def __init__(self):
        self._monitors = []
        self._parametersNames = {}
        self._getters = {}
        
    def registerMonitor(self, monitor):
        self._monitors.append(monitor)

    def actionStats(self, stats):
        for monitor in self._monitors:
            statsToAdd = []
            for stat in stats:
                if stat["agent"].__class__ in monitor.monitoredAgentClasses():
                    statsToAdd.append(stat)
            monitor.actualStats(statsToAdd)
            
    def printAgregatedValues(self):
        for monitor in self._monitors:
            monitor.printAgregatedValue()