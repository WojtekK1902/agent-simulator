from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.MonitorHelper import getCenterOfGravity, getDist
from monitor.StatsMonitor import StatsMonitor


class CenterOfGravityMoveMonitor(StatsMonitor):
        
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._max = []
        self._sum = []
        self._count = []
        self._prevCoG = []
        
    def getParametersNames(self):
        return ['genotypes']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        stats = []
        for index in xrange(Parameters.herdAgentsCount):
            stats.append(self._getStats(index))
        maxVal = stats[0][2]
        sumVal = 0
        count = 0
        for stat in stats:
            maxVal = max(maxVal ,stat[2])
            sumVal += stat[0]
            count += stat[1]
        if count == 0:
            average = sumVal
        else:
            average = sumVal/count
        print "Summary Max shift of center of gravity: "+str(maxVal)
        print "Summary Avg shift of center of gravity: "+str(average)
        
    def _getStats(self, index):
        maxVal = self._max[index]
        sumVal = self._sum[index]
        count = self._count[index]
        if count == 0:
            avgVal = sumVal
        else:
            avgVal = sumVal/count
        if Parameters.printHerdStats:
            print "Herd "+str(index)
            print "Max shift of center of gravity: "+str(maxVal)
            print "Avg shift of center of gravity: "+str(avgVal)
        return [sumVal, count, maxVal]
            
    def actualStats(self, stats):
        genotypes = stats['genotypes']
        for i in xrange(len(genotypes)):
            herd_genotypes = genotypes[i]
            CoG = getCenterOfGravity(herd_genotypes)
            if len(self._prevCoG) <= i:
                self._prevCoG.insert(i, CoG)
                self._sum.insert(i, 0)
                self._count.insert(i, 0)
            prevCoG = self._prevCoG[i]
            dist = getDist(prevCoG, CoG)
            if len(self._max) <= i:
                maxVal = dist
            else:
                maxVal = self._max[i]
            maxVal = max(maxVal, dist)
            self._max[i] = maxVal
            sumVal = self._sum[i]
            self._sum[i] = sumVal + dist
            count = self._count[i] 
            self._count[i] = count + 1
            self._prevCoG[i] = CoG  
            
    def printStats(self, stats):
        return
    