from implementation.Parameters import Parameters
from numpy import *


class Mutation(object):
    
    def mutate(self, genotype, rand, meanIslandEnergy, meanParentsEnergy):
        if Parameters.mutation == 'adaptiveMutation':
            return getattr(self, Parameters.mutation)(genotype, rand, meanIslandEnergy, meanParentsEnergy)
        else:
            return getattr(self, Parameters.mutation)(genotype, rand)
    
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
    
    def normalDistribution(self, genotype, rand):
        i = rand.randint(0, Parameters.genotypeLength-1)
        mutation = rand.normalvariate(0, 1)
        mutation *= Parameters.mutationMaxValue
        if rand.randint(0, 100) > 50:
            sign = 1
        else:
            sign = -1
        newValue = genotype[i] + sign * mutation
  
        if newValue > Parameters.cubeSize:
            newValue = Parameters.cubeSize
        if newValue < -Parameters.cubeSize:
            newValue = -Parameters.cubeSize
        genotype[i] = newValue
        return genotype

    def discreteDistribution1n1(self, genotype, rand):
        i = rand.randint(0, Parameters.genotypeLength-1)        
        genotype[i] = -genotype[i]
        return genotype

    def discreteFlip(self, genotype, rand):
        i=j=0
        while i==j:
            i = rand.choice(range(0,len(genotype)-1))        
            i = rand.choice(range(0,len(genotype)-1))
        temp = genotype[i]
        genotype[i] = genotype[j]
        genotype[j]=temp

        return genotype

    def adaptiveMutation(self, genotype, rand, meanIslandEnergy, meanParentsEnergy):
        i = rand.randint(0, Parameters.genotypeLength-1)
        #print abs(meanIslandEnergy-meanParentsEnergy)
        mutation = rand.normalvariate(0, 1)
        mutation *= Parameters.mutationMaxValue
        if rand.randint(0, 100) > 50:
            sign = 1
        else:
            sign = -1
        newValue = genotype[i] + sign * mutation

        if newValue > Parameters.cubeSize:
            newValue = Parameters.cubeSize
        if newValue < -Parameters.cubeSize:
            newValue = -Parameters.cubeSize
        genotype[i] = newValue
        return genotype


class SolisWetsMutation(object):
# wziete stad: http://sci2s.ugr.es/publications/ficheros/2010-SOCO-Molina-MA-SSW-Chains.pdf (Solis Wets)
    def mutate(self, genotype, rand, bias, fitness):        
        rho=Parameters.memeticRho
        dif=[]
        gen=genotype
        mybias=bias
        numSuccess=0
        numFailed=0
        
        for evals in xrange(0,Parameters.memeticMaxEvals-1):
            for i in xrange(0,Parameters.genotypeLength):
                dif.append(rand.normalvariate(0,rho))
            newgen = addGenotypes(mybias, addGenotypes(gen, dif))
            if fitness(newgen)<fitness(gen):
                gen=newgen
                mybias = multiplyGenotype(mybias, 0.2)+multiplyGenotype(addGenotypes(dif, mybias), 0.4)
                numSuccess+=1
                numFailed=0
            else:
                newgen=substractGenotypes(substractGenotypes(gen, dif),mybias)
                if fitness(newgen)<fitness(gen):
                    gen=newgen
                    mybias=substractGenotypes(mybias, multiplyGenotype(addGenotypes(dif, mybias), 0.4))
                    numSuccess+=1
                    numFailed=0
                else:
                    numFailed+=1
                    numSuccess=0
            
            if numSuccess>5:
                rho*=2
                numSuccess=0
            elif numFailed>3:
                rho/=2
                numFailed=0
        return gen

class IsotropicMutation(object):
# wziete stad: http://www.mlahanas.de/Math/nsphere.htm
    def mutate(self, genotype, rand, bias, fitness):                        
        gen=genotype
        bestgen = genotype      
                
        for evals in xrange(0,Parameters.memeticMaxEvals-1):            
            newgen=addGenotypes(genotype,self.pointOnSphereScaled(rand))            
            if fitness(newgen)<fitness(bestgen):                
                bestgen=newgen                
        return bestgen

    def pointOnSphereScaled(self,rand):
        r=0
        dif=[]
        for i in xrange(0,Parameters.genotypeLength):
            g=rand.normalvariate(0,1)
            dif.append(g)
            r += dif[i]*dif[i]
        r=sqrt(r)
        for i in xrange(0,Parameters.genotypeLength):
            dif[i] = dif[i] * Parameters.memeticRho / r #rzut na sfere oraz od razu skalujemy
        return dif            
        

class BrentMutation(object):
    # wziete stad: http://www.inf.ethz.ch/personal/vroth/wrk/problem1_4.pdf
    #http://linneus20.ethz.ch:8080/1_5_2.html
    # niestety ten operator wyraznie preferuje poczatek ukladu wsp
    def mutate(self, genotype, rand, bias, fitness):                
        dif=[]
        gen=genotype
        h0 = 0.1 #(parametr)
        
        h1 = 0  
        h2 = h0
        h3 = h1 + 1.62 * h0


        # tworzymy wektor jednostkowy
        for i in xrange(0,Parameters.genotypeLength):
            dif.append(rand.normalvariate(0,1))
        difLen=lenGenotype(dif)        
        for i in xrange(0,Parameters.genotypeLength):
            dif[i]/=difLen
        
        f1=fitness(gen)
        f2=fitness(addGenotypes(gen, multiplyGenotype(dif,h2)))
        f3=fitness(addGenotypes(gen, multiplyGenotype(dif,h3)))

        if ((f1 > f2) and (f2 > f3)) or ((f1 < f2) and (f2 < f3)):
            for i in xrange(10):                            
                if ((f1 > f2) and (f2 > f3)):            
                    x = 1.62 *(h3 - h2)+ h3
                    h1 = h2
                    h2 = h3
                    h3 = x
                elif ((f1 < f2) and (f2 < f3)):
                    x = h1- 1.62 *(h2 - h1)
                    h3 = h2
                    h2 = h1
                    h1 = x
                if not ((f1 > f2) and (f2 > f3)) or ((f1 < f2) and (f2 < f3)):
                    break
        
        if ((f1 > f2) and (f2 > f3)) or ((f1 < f2) and (f2 < f3)):            
            return gen    
        
        [h1p,h2p,h3p] = self.brentStep(h1,h2,h3,fitness,gen,dif)
        print "sukces"
        return multiplyGenotype(gen,h2p)
           
        
    def brentStep(self, ax,bx,cx, fitness, gen,dif):
        C = (3-sqrt(5))/2;
        R = 1-C;
    
        x0 = ax;
        x3 = cx;
        if (abs(cx-bx) > abs(bx-ax)):
            x1 = bx
            x2 = bx + C*(cx-bx)
        else:
            x2 = bx
            x1 = bx - C*(bx-ax)
        
        f1 = fitness(addGenotypes(gen, multiplyGenotype(dif,x1)))
        f2 = fitness(addGenotypes(gen, multiplyGenotype(dif,x2)))            
        
        if f2 < f1:
            x0 = x1
            x1 = x2
            x2 = R*x1 + C*x3 #;   % x2 = x1+c*(x3-x1)
            f1 = f2
            f2 = fitness(addGenotypes(gen, multiplyGenotype(dif,x2)))
        else:
            x3 = x2
            x2 = x1
            x1 = R*x2 + C*x0#;   % x1 = x2+c*(x0-x2)
            f2 = f1
            f1 = fitness(addGenotypes(gen, multiplyGenotype(dif,x1)))
        
         
        if f1 < f2:              
            return [x0,x1,x2]
        else:              
            return [x3,x2,x1]
        
            
                        

            
         
            
            
            
            

            


def addGenotypes(gen1,gen2):
    ret=[]
    for i in xrange(0,Parameters.genotypeLength):
         ret.append(gen1[i]+gen2[i])
    return ret

def substractGenotypes(gen1,gen2):
    ret=[]
    for i in xrange(0,Parameters.genotypeLength):
         ret.append(gen1[i]-gen2[i])
    return ret

def multiplyGenotype(gen1,a):
    ret=[]
    for i in xrange(0,Parameters.genotypeLength):
         ret.append(gen1[i]*a)
    return ret

def lenGenotype(gen1):
    ret=0
    for i in xrange(0,Parameters.genotypeLength):
         ret+=gen1[i]*gen1[i]
    return sqrt(ret)
