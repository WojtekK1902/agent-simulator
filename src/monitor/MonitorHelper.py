from implementation.Parameters import Parameters
from numpy.lib.scimath import power, sqrt

def getCenterOfGravity(genotypes):
    centerOfGravity = []
    for i in xrange(Parameters.genotypeLength):
        centerOfGravity.append(0)
    count = 0
    for genotype in genotypes:
        for i in xrange(len(genotype)):
            centerOfGravity[i] += genotype[i]
        count += 1
    for i in xrange(len(centerOfGravity)):
        centerOfGravity[i] = centerOfGravity[i]/count
    return centerOfGravity
    
def getDist(point1, point2):
    sumVal = 0
    for i in xrange(len(point1)):
        sumVal += power(point1[i]+point2[i],2)
    return sqrt(sumVal)