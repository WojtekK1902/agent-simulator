from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from monitor.StatsMonitor import StatsMonitor

class SimStepsToMakeResultBetterMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._sum = []
        self._count = []
        self._previousBestFitness = []
        self._actualStepsNr = []
        self._maxNrOfSteps = []
    
    def getParametersNames(self):
        return ['fitnesses']
         
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
        print "Summary Avg num of steps to make result better: "+str(average)
        print "Summary Max num of steps to make result better: "+str(maxVal)
        
        
    def _getStats(self, index):
        sumVal = self._sum[index]
        count = self._count[index]
        if count == 0:
            average = sumVal
        else:
            average = sumVal/count
        maxVal = self._maxNrOfSteps[index]
        if Parameters.printHerdStats:
            
            print "Herd "+str(index)
            print "Avg num of steps to make result better: "+str(average)
            print "Max num of steps to make result better: "+str(maxVal)
        return [sumVal, count, maxVal]
        
    def printStats(self, stats):
        return
    
    def actualStats(self, stats):
        fitnesses = stats['fitnesses']
        for i in xrange(len(fitnesses)):
            herd_fitnesses = fitnesses[i]
            if len(self._previousBestFitness) <= i:
                bestRes = None
            else:
                bestRes = self._previousBestFitness[i]
            for fitness in herd_fitnesses:
                if bestRes is None or fitness < bestRes:
                    bestRes = fitness
            if len(self._previousBestFitness) <= i:
                self._previousBestFitness.insert(i, bestRes)
                self._actualStepsNr.insert(i, 1)
                self._count.insert(i, 0)
                self._sum.insert(i, 0.0)
            else:
                if bestRes < self._previousBestFitness[i]:
                    stepsSum = self._sum[i]
                    self._sum[i] =  stepsSum + self._actualStepsNr[i]
                    if len(self._maxNrOfSteps) <= i:
                        self._maxNrOfSteps.insert(i, self._actualStepsNr[i])
                    else:
                        maxNrOfSteps = self._maxNrOfSteps[i]
                        if maxNrOfSteps < self._actualStepsNr[i]:
                            self._maxNrOfSteps[i] = self._actualStepsNr[i]
                    self._actualStepsNr[i] = 1
                    self._previousBestFitness[i] = bestRes
                    count = self._count[i]
                    self._count[i] = count + 1
                else:
                    count = self._actualStepsNr[i]
                    self._actualStepsNr[i] = count + 1
                    