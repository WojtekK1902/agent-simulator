from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.StatsMonitor import StatsMonitor

class PopulationCountMonitor(StatsMonitor):
        
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._maxes = []
        self._mins = []
        self._counts = []
        self._steps = 0
        self.ofile = open('count.txt', 'a')

    def __del__(self):
        self.ofile.close()
       
    def getParametersNames(self):
        return ['count']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        print 'Max count: %d' % max(self._maxes)
        print 'Min count: %d' % min(self._mins)
        print 'Avg count: %.3f' % (float(sum(self._counts)) / (self._steps * len(self._counts)))
        if Parameters.printHerdStats:
            self.printStats(None)
            
    def printStats(self, stats):
        for i in xrange(len(self._counts)):
            print 'Herd %d:' % (i)
            print 'Max count: %d' % self._maxes[i]
            print 'Min count: %d' % self._mins[i]
            print 'Avg count: %.3f' % (float(self._counts[i]) / self._steps)
            
    def actualStats(self, stats):
        counts = stats['count']
        for i in xrange(len(counts)):
            try:
                self._counts[i] += counts[i]
                self._maxes[i] = max(counts[i], self._maxes[i])
                self._mins[i] = min(counts[i], self._mins[i])
            except:
                self._counts.append(counts[i])
                self._maxes.append(counts[i])
                self._mins.append(counts[i])
        
        if(self._steps % Parameters.statsCollectFreq == 0):
            print str(counts)
            sum = 0
            for c in counts:
                sum+=c
            self.ofile.write(str(self._steps)+";"+str(sum)+"\n")
        
        self._steps += 1       
        
