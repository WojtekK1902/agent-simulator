from monitor.StatsMonitor import StatsMonitor


class EnergyHistogramMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._num = 0
        self._histogramStatsCollectSteps = [100, 1000, 2000, 2900]
    
    def getParametersNames(self):
        return ['energies']
    
    def printAgregatedValue(self):
        pass
       
    def actualStats(self, stats):
        self._num += 1

        if self._num in self._histogramStatsCollectSteps:
            energies = stats['energies']
            all_energies = []
            for e in energies:
                all_energies.extend(e)

            all_energies.sort()
            ofile = open('energy_histogram_' + str(self._num) + '.txt', 'w')
            for e in all_energies:
                ofile.write(str(e) + '\n')
            ofile.close()