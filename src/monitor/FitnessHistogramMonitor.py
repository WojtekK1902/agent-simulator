from monitor.StatsMonitor import StatsMonitor


class FitnessHistoryMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._num = 0
        self._histogramStatsCollectSteps = [100, 1000, 2000, 2900]
    
    def getParametersNames(self):
        return ['fitnesses']    
    
    def printAgregatedValue(self):
        pass
       
    def actualStats(self, stats):
        self._num += 1

        if self._num in self._histogramStatsCollectSteps:
            fitnesses = stats['fitnesses']
            all_fitnesses = []
            for e in fitnesses:
                all_fitnesses.extend(e)

            all_fitnesses.sort()
            ofile = open('fitness_histogram_' + str(self._num) + '.txt', 'w')
            for e in all_fitnesses:
                ofile.write(str(e) + '\n')
            ofile.close()