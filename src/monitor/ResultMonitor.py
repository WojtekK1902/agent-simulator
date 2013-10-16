from implementation.HerdAgent import HerdAgent
from monitor.StatsMonitor import StatsMonitor
from implementation.Parameters import Parameters

class ResultMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._bestResults = []
        self._bestGenotypes = []
    
    def getParametersNames(self):
        return ['fitnesses', 'genotypes']    
    
    def printAgregatedValue(self):
        stats = []
        for index in xrange(Parameters.herdAgentsCount):
            stats.append(self._getStats(index))
        best = stats[0][0]
        bestResult = stats[0]
        for stat in stats:
            if stat[0] < best:
                best = stat[0]
                bestResult = stat
                
        print "Summary Result: " + str(bestResult[0])
        print "Summary Best genotype: "+ str(bestResult[1])
        
    def _getStats(self, index):
        if Parameters.printHerdStats:
            print "Herd "+str(index)
            print "Result: " + str(self._bestResults[index])
            print "Best genotype: "+ str(self._bestGenotypes[index])
            
        return [self._bestResults[index], self._bestGenotypes[index]]
            
    def printStats(self, stats):
        return
            
    def actualStats(self, stats):
        fitnesses = stats['fitnesses']
        genotypes = stats['genotypes']
        for i in xrange(0,len(fitnesses)):
            herd_fitnesses = fitnesses[i]
            if len(self._bestResults) <= i:
                bestFitness = None
                self._bestResults.insert(i, 0)
            else:
                bestFitness = self._bestResults[i]
            for j in xrange(len(herd_fitnesses)):
                fitness = herd_fitnesses[j]
                if bestFitness is None or fitness < bestFitness:
                    self._bestResults[i] = fitness
                    self._bestGenotypes.insert(i, genotypes[i][j])
