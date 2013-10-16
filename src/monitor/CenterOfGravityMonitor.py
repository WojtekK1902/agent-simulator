from monitor.StatsMonitor import StatsMonitor
from implementation.HerdAgent import HerdAgent
from monitor.MonitorHelper import getCenterOfGravity

class CenterOfGravityMonitor(StatsMonitor):

    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)

    def getParametersNames(self):
        return ['genotypes']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        print '%s - it is not supposed to be aggregated. Try printStats.' % (self.__class__.__name__)
    
    def printStats(self, stats):
        allGenotypes = stats['genotypes']
        summaryGenotypes = []
        count = 0
        for genotypes in allGenotypes:
            centerOfGravity = getCenterOfGravity(genotypes)
            summaryGenotypes += genotypes
            print "Herd "+str(count)
            count += 1
            print "CenterOfGravity: ", centerOfGravity
        print "Summary CenterOfGravity: ", getCenterOfGravity(summaryGenotypes)
        
    def actualStats(self, stats):
        pass