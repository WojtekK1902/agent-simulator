from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.StatsMonitor import StatsMonitor

class DieAndReproductionMonitor(StatsMonitor):

    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._reproduceCounts = []
        self._dieCounts = []
        self._steps = 0
        self.ofile = open('reproduceCount.txt', 'a')

    def __del__(self):
        self.ofile.close()

    def getParametersNames(self):
        return ['dieCount', 'reproduceCount']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        print 'Avg deaths count per step: %.3f' % (
            float(sum(self._dieCounts)) / (self._steps * len(self._dieCounts)))
        print 'Avg reproductions count per step: %.3f' % (
            float(sum(self._reproduceCounts)) / (self._steps * len(self._reproduceCounts)))

        if Parameters.printHerdStats:
            self.printStats(None)

    def printStats(self, stats):
        for i in xrange(len(self._dieCounts)):
            print 'Herd %d:' % (i)
            print 'Avg deaths count per step: %.3f' % (
                float(self._dieCounts[i]) / self._steps)
            print 'Avg reproductions count per step: %.3f' % (
                float(self._reproduceCounts[i]) / self._steps)

    def actualStats(self, stats):
        stats_repr = stats['reproduceCount']
        stats_die = stats['dieCount']
        
        for i in xrange(len(stats_repr)):
            try:
                self._dieCounts[i] += stats_die[i]
                self._reproduceCounts[i] += stats_repr[i]
            except:
                self._dieCounts.append(stats_die[i])
                self._reproduceCounts.append(stats_die[i])

        if(self._steps % Parameters.statsCollectFreq == 0):
            print str(stats_repr)
            sum = 0
            for c in stats_repr:
                sum+=c
            if Parameters.memetics=='Baldwin':
                self.ofile.write(str(self._steps)+";"+str(100*sum)+"\n")
            else:
                self.ofile.write(str(self._steps)+";"+str(sum)+"\n")

        self._steps += 1
