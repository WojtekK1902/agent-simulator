from simulation.SimLogic import SimLogic
from implementation.Parameters import Parameters
from monitor.StatsMonitor import StatsMonitor
from implementation.HerdAgent import HerdAgent

class StatsCollector(StatsMonitor):
    
    def __init__(self, agent_class,filename='stats.txt'):
        StatsMonitor.__init__(self, agent_class)
        import os
        self.filename = filename
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        self._meetingsSum = 0.0
        self._fightsSum = 0.0
        self._reproduceSum = 0.0
        self._maxAge = 0
        self._minAge = 1000
        self._ageSum = 0.0
        self._successMeetingsSum = 0.0
            
    def getParametersNames(self):
        return ['meetings','fights','reproduceCount','age','genotypes','dieAge']
         
    def getAgentClass(self):
        return HerdAgent
    
    def printAgregatedValue(self):
        pass
      
    def printStats(self, params):
        timestamp = SimLogic.timestamp
        self._meetingsSum += params['meetings']
        self._fightsSum += params['fights']
        self._reproduceSum += params['reproduceCount']
        avgAge = 0.0
        for age in params['age']:
            avgAge += age
            if age > self._maxAge:
                self._maxAge = age
        for age in params['dieAge']:
            age = timestamp - age
            if age < self._minAge:
                self._minAge = age
        avgAge /= len(params['age'])
        self._ageSum += avgAge
        successMeetings = params['fights'] + params['reproduceCount']
        self._successMeetingsSum += successMeetings
        if timestamp != 0 and timestamp % Parameters.statsCollectFreq == 0:
            f = open(self.filename, 'a')
            f.write("timestamp: " + str(timestamp) + "\n")
            f.write("avg meetings = " + str(self._meetingsSum/timestamp)+ "\n")
            f.write("avg successful meetings = " + str(self._successMeetingsSum/timestamp)+ "\n")
            f.write("avg fights = " + str(self._fightsSum/timestamp)+ "\n")
            f.write("avg reproductions = " + str(self._reproduceSum/timestamp)+ "\n")
            f.write("avg age = " + str(self._ageSum/timestamp)+ "\n")
            f.write("max age = " +str(self._maxAge)+ "\n")
            f.write("min age = " + str(self._minAge) + "\n")
            f.write("genotypes:\n")
            for genotype in params['genotypes']:
                s = ''
                for i in xrange(Parameters.genotypeLength):
                    s += str(genotype[i]) + ' '
                f.write(s)
                f.write("\n")
            f.write("\n")
            f.close()
    
    def actualStats(self, stats):
        pass