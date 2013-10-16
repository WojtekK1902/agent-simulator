'''
Created on 2012-07-18

@author: Bogusia
'''
from implementation.Parameters import *
from random import Random
from array import array
import math
from simulation.Global import *



class BaldwinFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):        
        fit=globals()[Parameters.baldwinFitness]()
        bestGenotype=genotype
        bestGenotypeFitness=fit.getFitness(genotype)
        for i in range(Parameters.memeticSteps):                
            bests=[]                
            for j in range(Parameters.memeticMutations):
                bests.append(self.continuousDistribution(bestGenotype,Random()))
            for gen in bests:
                f = fit.getFitness(gen)
                if f < bestGenotypeFitness:
                    bestGenotypeFitness=f
                    bestGenotype=gen
        return bestGenotypeFitness                    
    
            
    
    def continuousDistribution(self, genotype, rand):
        i = rand.randint(0, Parameters.genotypeLength-1)
        mutation = rand.random()
        while mutation > Parameters.mutationFactor:
            mutation = rand.random()
        if rand.randint(0, 100) > 50:
            sign = 1
        else:
            sign = -1
        mutation *= Parameters.mutationMaxValue
        newValue = genotype[i]+sign*mutation
        if newValue > Parameters.cubeSize:
            newValue = Parameters.cubeSize
        if newValue < -Parameters.cubeSize:
            newValue = -Parameters.cubeSize
        genotype[i] = newValue
        return genotype
    
    
    
    
class RastriginFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):        
        result = 0
        val = 2 * math.pi
        for el in genotype:
            result += (el * el - 10 * math.cos(val * el))
        result += 10 * len(genotype)
        return result

class FrequencyModulatedSoundWavesFitness():
    def __init__(self):
        '''
        Constructor
        '''

    def getFitness(self, genotype):
        theta = 2.0*math.pi/100.0
        f = 0.0
        for t in range(0,101):
            y_t=genotype[0]*math.sin(genotype[1]*t*theta+genotype[2]*math.sin(genotype[3]*t*theta+genotype[4]*math.sin(genotype[5]*t*theta)))
            y_0_t=math.sin(5.0*t*theta-1.5*math.sin(4.8*t*theta+2.0*math.sin(4.9*t*theta)))
            f += (y_t-y_0_t)**2
        return f

class RastriginDynamicFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):
        currentStep = Global().getStep()
        modifiers = array('f', [0, 0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2])
        
        
        mod= (currentStep // 1000)% len(modifiers)# co 1000 krokow robimy adaptacje fitn                 
        
        
        result = 0
        val = 2 * math.pi
        for el in genotype:
            result += ((el-modifiers[mod]) * (el-modifiers[mod]) - 10 * math.cos(val * (el-modifiers[mod])))
        result += 10 * len(genotype)
        return result

class DeJongFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):
        result = 0
        for el in genotype:
            result += el * el
        return result

class DeJongDynamicFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):
                
        currentStep = Global().getStep()
        modifiers = array('l', [0, 1, 2, 1])
        
        
        mod= (currentStep // 1000)% len(modifiers)# co 1000 krokow robimy adaptacje fitn         
                    
        result = 0
        for el in genotype:
            result += (el-modifiers[mod]) * (el-modifiers[mod])
        return result

class RosenbrockFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):
        assert Parameters.genotypeLength == 2
        x = genotype[0]
        y = genotype[1]
        return math.pow(1-x, 2) + 100*pow(y - x*x, 2)
    
class AckleyFitness():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getFitness(self,genotype):

        genSum = 0
        cos_sum = 0
        val = 2*math.pi
        for x_i in genotype:
            genSum += x_i * x_i
            cos_sum += math.cos(val*x_i)
        return -20*math.exp(-0.2*math.sqrt(genSum/Parameters.genotypeLength))-math.exp(cos_sum/Parameters.genotypeLength)+20+math.exp(1)
        
