from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.StatsMonitor import StatsMonitor

class ReadyToReproductionMonitor(StatsMonitor):
        
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._wantReproduceCounts = []
        self._steps = 0
        
    def getParametersNames(self):
        return ['wantReproduceCount']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        print 'Avg reproduction count per step: %.3f' % (
            float(sum(self._wantReproduceCounts)) / (self._steps * len(self._wantReproduceCounts)))
        self.printStats(None)
        
    def printStats(self, stats):
        for i in xrange(len(self._wantReproduceCounts)):
            print 'Herd %d:' % (i)
            print 'Avg ready to reproduction per step: %.3f' % (
                float(self._wantReproduceCounts[i]) / self._steps)

    def actualStats(self, stats):
        stats = stats['wantReproduceCount']
        
        for i in xrange(len(stats)):
            try:
                self._wantReproduceCounts[i] += stats[i]
            except:
                self._wantReproduceCounts.append(stats[i])

        self._steps += 1
