from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.StatsMonitor import StatsMonitor

class AgentStepsCountMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._agentsteps = []
    
    def getParametersNames(self):
        return ['count']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        print 'Agentsteps: %d' % (self.getAgentsSteps())
        if Parameters.printHerdStats:
            self.printStats(None)
        
    def printStats(self, stats):
        for i in xrange(len(self._agentsteps)):
            print 'Herd %d:' % (i)
            print 'Agentsteps: %d' % (self._agentsteps[i])
    
    def getAgentsSteps(self):
        return sum(self._agentsteps)
    
    def actualStats(self, stats):
        counts = stats['count']
        for i in xrange(len(counts)):
            try:
                self._agentsteps[i] += counts[i]
            except:
                self._agentsteps.append(counts[i])
