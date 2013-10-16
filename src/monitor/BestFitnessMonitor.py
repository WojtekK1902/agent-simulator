from monitor.StatsMonitor import StatsMonitor
from numpy.lib.scimath import sqrt
from implementation.Parameters import Parameters

class BestFitnessMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._num = 0
        self._bestResults = []
        self.ofile = open('fitness.txt', 'a')
    def __del__(self):
        self.ofile.close()
    
    def getParametersNames(self):
        return ['fitnesses']    
    
    def printAgregatedValue(self):
        pass
       
    def actualStats(self, stats):
        if(self._num % Parameters.statsCollectFreq != 0):
            self._num += 1
            return
        fitnesses = stats['fitnesses']
        self._bestResults=[]        
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
        
        bf = None
        for i in xrange(0,len(self._bestResults)):
            if bf is None or self._bestResults[i]<bf:
                bf=self._bestResults[i]
        print "BF:\t"+str(self._num)+"\t"+str(bf)
        self.ofile.write(str(self._num)+";"+str(bf)+"\n")
              
        
        self._num += 1