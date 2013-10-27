from monitor.StatsMonitor import StatsMonitor
from implementation.Parameters import Parameters
from numpy import mean

class ReproductionHistoryMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._num = 0
        self._bestResults = []
        self._lastReproductionsCount = 200 #how many recent reproductions are taken to statistics
        self.ofile = open('reproductionHistory.txt', 'a')
    def __del__(self):
        self.ofile.close()
    
    def getParametersNames(self):
        return ['reproductionHistory']
    
    def printAgregatedValue(self):
        pass
       
    def actualStats(self, stats):
        if(self._num % Parameters.statsCollectFreq != 0):
            self._num += 1
            return
        reprHistory = stats['reproductionHistory']

        meanSuccesses = []
        for i in xrange(0,len(reprHistory)):
            if len(reprHistory[i]) < self._lastReproductionsCount:
                meanSuccesses.append(mean(reprHistory[i]))
            else:
                meanSuccesses.append(mean(reprHistory[i][-self._lastReproductionsCount:]))

        print meanSuccesses

        self.ofile.write(str(self._num) + ';' + str(mean(meanSuccesses)) + '\n')

        self._num += 1