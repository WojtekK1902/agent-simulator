from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.MonitorHelper import getCenterOfGravity, getDist
from monitor.StatsMonitor import StatsMonitor

class DistFromCoGMonitor(StatsMonitor):
        
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._min = []
        self._max = []
        
    def getParametersNames(self):
        return ['genotypes']
         
    def getAgentClass(self):
        return HerdAgent
    
    
    def printAgregatedValue(self):
        stats = []
        for index in xrange(Parameters.herdAgentsCount):
            stats.append(self._getStats(index))
        maxVal = stats[0][1]
        minVal = stats[0][0]
        for stat in stats:
            maxVal = max(maxVal ,stat[1])
            minVal = min(minVal, stat[0])
        print "Summary Min dist from center of gravity " + str(minVal)
        print "Summary Max dist from center of gravity " + str(maxVal)
        
    def _getStats(self, index):
        if Parameters.printHerdStats:
            print "Herd "+str(index)
            print "Min dist from center of gravity " + str(self._min[index])
            print "Max dist from center of gravity " + str(self._max[index])
        return [self._min[index], self._max[index]]
    
    
    def actualStats(self, stats):
        genotypes = stats['genotypes']
        for i in xrange(len(genotypes)):
            herd_genotypes = genotypes[i]
            if len(self._min) <= i:
                maxVal = None
                minVal = None
                self._min.insert(i, 0)
                self._max.insert(i, 0)
            else:
                maxVal = self._max[i]
                minVal = self._min[i]
            CoG = getCenterOfGravity(herd_genotypes)
            maxDist = getDist(herd_genotypes[0], CoG)
            minDist = maxDist
            for i in xrange(1, len(herd_genotypes)):
                dist = getDist(herd_genotypes[i], CoG)
                maxDist = max(maxDist, dist)
                minDist = min(minDist, dist)
            if maxVal is None:
                maxVal = maxDist
                minVal = minDist
            maxVal = max(maxVal, maxDist)
            minVal = min(minVal, minDist)
            self._min[i] = minVal
            self._max[i] = maxVal
    
            
    def printStats(self, stats):
        return
            
    