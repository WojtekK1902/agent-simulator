from monitor.StatsMonitor import StatsMonitor
from numpy.lib.scimath import sqrt
from implementation.Parameters import Parameters

class EnergyMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._num = 0
        self._bestResults = []
        self.ofiles = []
        self._maxes = []
        self._mins = []
        self._steps = 0
        for i in range(Parameters.herdAgentsCount):
            self.ofiles.append(open('energy' + str(i + 1) +'.txt', 'a'))
        self._energies = []
    def __del__(self):
        for file in self.ofiles:
            file.close()
    
    def getParametersNames(self):
        return ['energies']
    
    def printAgregatedValue(self):
        pass
       
    def actualStats(self, stats):
        energies = stats['energies']
        for i in xrange(len(energies)):
            try:
                self._energies[i] += energies[i]
                self._maxes[i] = max(energies[i], self._maxes[i])
                self._mins[i] = min(energies[i], self._mins[i])
            except:
                self._energies.append(energies[i])
                self._maxes.append(energies[i])
                self._mins.append(energies[i])

        if(self._steps % Parameters.statsCollectFreq == 0):
            print str(energies)
            for i, e in enumerate(energies):
                self.ofiles[i].write(str(self._steps)+";"+str(e)+"\n")

        self._steps += 1
              
        
        self._num += 1