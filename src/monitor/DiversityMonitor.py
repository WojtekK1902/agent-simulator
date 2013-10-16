from monitor.StatsMonitor import StatsMonitor
from numpy.lib.scimath import sqrt
from implementation.Parameters import Parameters

class DiversityMonitor(StatsMonitor):
    
    def __init__(self, agent_class):
        StatsMonitor.__init__(self, agent_class)
        self._num = 0
        self.ofile = open('diversity.txt', 'a')
        
    def __del__(self):
        self.ofile.close()
    
    def getParametersNames(self):
        return ['genotypes']    
    
    def printAgregatedValue(self):
        pass
       
    def actualStats(self, stats):
        if(self._num % Parameters.statsCollectFreq != 0):
            self._num += 1
            return
        genotypes = stats['genotypes']
        herds_max = []
        sumJongVal = 0.0
        jongValues = []
        for i in xrange(0,len(genotypes)):
            herd_genotypes = genotypes[i]
            avgVals = []
            powSumVals = []
            herd_genotypes_len = len(herd_genotypes) - 1
            genotype_len = Parameters.genotypeLength-1
            for j in xrange(genotype_len):
                avgVals.append(0)
                powSumVals.append(0)
            for j in xrange(herd_genotypes_len):
                genotype = herd_genotypes[j]
                for g in xrange(genotype_len):
                    gen = genotype[g]
                    avgVals[g] += gen
                    powSumVals[g] += gen * gen
            values = []
            for j in xrange(genotype_len):
                avgVals[j] = avgVals[j]/herd_genotypes_len
                avgVal = avgVals[j]
                values.append(sqrt(powSumVals[j]/herd_genotypes_len-avgVal*avgVal))
            
            jongValue = 0.0
            for j in xrange(herd_genotypes_len):
                genotype = herd_genotypes[j]
                for k in xrange(genotype_len):
                    val = (genotype[k]-avgVals[k])*(genotype[k]-avgVals[k])
                    jongValue += val
                    sumJongVal += val
            jongValues.append(jongValue)
            herds_max.append(max(values))
        
        
        if Parameters.printHerdStats:
            for i in xrange(len(herds_max)):
                print "Herd "+str(i)
                print "Diversity: "+str(self._num)+" "+str(herds_max[i]) +" "+str(jongValues[i])
        print "Summary diversity: "+str(self._num)+" "+str(max(herds_max)) +" "+str(sumJongVal)
        self.ofile.write(str(self._num)+";"+str(max(herds_max)) +";"+str(sumJongVal)+"\n")
        self._num += 1