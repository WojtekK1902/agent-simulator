from agent.Agent import Agent
from implementation.Parameters import *
from mutation.Mutation import *
from random import Random
from array import array
import math
from simulation.Global import Global
from machine_learning.AQMemetizationManager import AQMemetizationManager
from machine_learning.NBMemetizationManager import NBMemetizationManager
from numpy import mean

class Specimen(Agent):

    def __init__(self, id, env):        
        Agent.__init__(self, id, env)
        self._energy = Parameters.initEnergy
        self._reproductionMinEnergy = Parameters.reproductionMinEnergy
        self._genotype = []
        self._rand = Random()                
        getattr(self, "_initialization"+Parameters.initialization)()
        self._fitness=None
        self._updated=None
        self._recalculateFitness()
        self._fitnessCalls = 0
        self._lost = 0
        self._won = 0
        
    def _initializationREAL(self):
        rand = self._rand
        for i in xrange(Parameters.genotypeLength):
            if rand.randint(0, 100) > 50:
                self._genotype.append(Parameters.cubeSize * rand.random())
            else:
                self._genotype.append(-1 * Parameters.cubeSize * rand.random())

    def _initializationDISCRETE1n1(self):
        rand = self._rand
        for i in xrange(Parameters.genotypeLength):
            if rand.randint(0, 100) > 50:
                self._genotype.append(1)
            else:
                self._genotype.append(-1)

    def _initializationPERMUTATION(self):
        rand = self._rand
        #self._genotype=list(range(Parameters.genotypeLength))
        self._genotype=[i for i in range(Parameters.genotypeLength)]
        rand.shuffle(self._genotype)

    def _initializationPERMUTATIONJS2(self):
        rand = self._rand
        #self._genotype=list(range(Parameters.genotypeLength))
        gen=[i for i in range(Parameters.genotypeLength)]
        for j in range(Parameters.genotypeLength):
            self._genotype+=gen
        rand.shuffle(self._genotype)
        a=1

               
#        rand = self._rand
#        for i in xrange(Parameters.genotypeLength):
#            self._genotype.append(i)
#        self._genotype=rand.shuffle(self._genotype)
#        return 0

    
    def _recalculateFitness(self):
        self._fitness = getattr(self, "_get"+Parameters.function+"Fitness")(self._genotype)
        self._updated=Global().getStep()
    
    def getFitness(self):
        if self._updated!=Global().getStep():
            self._recalculateFitness()
        return self._fitness
        #return getattr(self, "_get"+Parameters.function+"Fitness")()
        
    
    def _getRastriginFitness(self,gen):
        result = 0
        val = 2 * math.pi
        for el in gen:
            result += (el * el - 10 * math.cos(val * el))
        result += 10 * len(gen)
        return result

    def _getFrequencyModulatedSoundWavesFitness(self,genotype):
        theta = 2.0*math.pi/100.0
        f = 0.0
        for t in range(0,101):
            y_t=genotype[0]*math.sin(genotype[1]*t*theta+genotype[2]*math.sin(genotype[3]*t*theta+genotype[4]*math.sin(genotype[5]*t*theta)))
            y_0_t=math.sin(5.0*t*theta-1.5*math.sin(4.8*t*theta+2.0*math.sin(4.9*t*theta)))
            f += (y_t-y_0_t)**2
        return f

    def _getLABSFitness(self,gen):
        result = 0
        for i in xrange(len(gen)-1):        
            result += self._getLABSAutocorrelation(gen,i)         
        return result
    
    def _getLABSAutocorrelation(self,gen,k):
        result=0
        for i in xrange(len(gen)-k):
            result+=gen[i]*gen[i+k]
        return result

    def _getJobShopFitness(self,gen):
        MACHINES= 5
        JOBS = 10
        # operations/job = machines = 5
        
        jobsdef = [ 
                [[1, 21], [0, 53], [4, 95], [3, 55], [2, 34]],
                [[0, 21], [3, 52], [4, 16], [2, 26], [1, 71]],
                [[3, 39], [4, 98], [1, 42], [2, 31], [0, 12]],
                [[1, 77], [0, 55], [4, 79], [2, 66], [3, 77]],
                [[0, 83], [3, 34], [2, 64], [1, 19], [4, 37]],
                [[1, 54], [2, 43], [4, 79], [0, 92], [3, 62]],
                [[3, 69], [4, 77], [1, 87], [2, 87], [0, 93]],
                [[2, 38], [0, 60], [1, 41], [3, 24], [4, 83]],
                [[3, 17], [1, 49], [4, 25], [0, 44], [2, 98]],
                [[4, 77], [3, 79], [2, 43], [1, 75], [0, 96]]
                ]
        
        jobs = []
                
        machines = [-1 for i in range(MACHINES)]
        time = 0
        
        if Parameters.jobShopGenotype=='SimplePermutation':        
            #kolejnosc zadan zgodna z genotypem
            for jnum in gen:                
                jobs.append(jobsdef[jnum])
        else:
            jobs = jobsdef
            
                    
        
        while True:
            # przydzial taskow do wszystkich wolnych maszyn
            if Parameters.jobShopGenotype=='SimplePermutation':
                self._assignJobs(machines, jobs)
            else:
                self._assignJobsJS2(machines, jobs, gen)
            for m in machines:
                if m != -1:
                    break
            else:
                break
            
            # wykonanie kolejnego kroku
            for mnum in range(len(machines)):
                jnum=machines[mnum]
                if jnum!=-1:
                    jobs[jnum][0][1]-=1
                    if jobs[jnum][0][1]==0:
                        machines[mnum]=-1
                        jobs[jnum].pop(0)
            time+=1

        return time
    
    def _assignJobs(self,machines,jobs):
        for mnum in range(len(machines)):
            if machines[mnum]==-1:                
                    for jnum in range(len(jobs)):
                        if len(jobs[jnum])>0 and jobs[jnum][0][0]==mnum and jobs[jnum][0][1]>0:
                            machines[mnum]=jnum
                            break
        
    def _assignJobsJS2(self,machines,jobs,gen):
        for mnum in range(len(machines)):
            if machines[mnum]==-1:
                    myjobs=[]                                                                        
                    for jnum in range(len(jobs)):
                        if len(jobs[jnum])>0 and jobs[jnum][0][0]==mnum and jobs[jnum][0][1]>0:
                            myjobs.append(jnum)
                    if len(myjobs)==0:
                        continue
                    for g in gen:
                        if g in myjobs:                      
                            machines[mnum]=g                            
        



    def _getRoyalRoadFitness(self,gen):
        s1 = [-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0]
        s2 = [0,0,0,0,-1,-1,-1,-1,0,0,0,0,0,0,0,0]
        s3 = [0,0,0,0,0,0,0,0,-1,-1,-1,-1,0,0,0,0]
        s4 = [0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1]
        s5 = [0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1]
        s6 = [-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0]
        s7 = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        o1 = o2 = o3 = o4 =4
        o5= o6 = 8
        o7 = 16
        
        ss=[s1,s2,s3,s4,s5,s6,s7]
        oo=[o1,o2,o3,o4,o5,o6,o7]
        
        result=0
        for i in xrange(len(ss)):
            result+= self._getRoyalRoadMatch(gen, ss[i]) * oo[i]
        return result
        
    def _getRoyalRoadMatch(self,gen,s):
        result = -1
        for i in xrange(len(gen)):
            if gen[i]!= s[i] and s[i]!=0:
                result=0 
        return result
            
                     


    def _getRastriginDynamicFitness(self,gen):
        currentStep = Global().getStep()
        modifiers = array('f', [0, 0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2])
        
        
        mod= (currentStep // 1000)% len(modifiers)# co 1000 krokow robimy adaptacje fitn                 
        
        
        result = 0
        val = 2 * math.pi
        for el in gen:
            result += ((el-modifiers[mod]) * (el-modifiers[mod]) - 10 * math.cos(val * (el-modifiers[mod])))
        result += 10 * len(gen)
        return result

    
    def _getDeJongFitness(self,gen):
        result = 0
        for el in gen:
            result += el * el
        return result
    
    # f(x)=0, x[i]=0
    def _getSumOfPowerFunctionsFitness(self,gen):
        result = 0
        for i in xrange(len(gen)):
            result += pow(abs(gen[i]),i+2)
        return result
    
    

    # f(x)=- n * 418.9829, x[i]=420.9687, x in -500-500 
    # uwaga - trzeba przestawic obszar poszukiwan
    def _getSchwefelFitness(self,gen):
        result = 0
        for el in gen:
            result += - el * sin(sqrt(abs(el)))
        return result


    # -10:10, min=0, x=[0]
    # ta i wiele innych wziete stad: http://www.geatbx.com/docu/fcnindex-01.html
    def _getAxisParallelHyperEllipsoidFitness(self,gen):
        result = 0
        for i in xrange(len(gen)):
            el = gen[i]        
            result += (i+1) * el * el
        return result
    
    # -65536:65536, min=0, x=[0]
    def _getRotatedHyperEllipsoidFitness(self,gen):
        result = 0
        for i in xrange(len(gen)):            
            res2=0
            for j in range(0,i):
                el = gen[j]        
                res2 += el
            result += res2 * res2
        return result
    
    # min x[i]=[5*i], f(x)=0
    def _getMovedAxisParallelHyperEllipsoidFitness(self,gen):
        result = 0
        for i in xrange(len(gen)):
            el = gen[i]        
            result += 5* (i+1) * el * el
        return result
    
    # X in -600-600, f(x)=0, x[i]=0
    def _getGriewangkFitness(self,gen):
        sum1 = 0
        prod = 1
        for i in xrange(len(gen)):
            sum1 += (gen[i]*gen[i])/4000
            prod *= cos(gen[i]/sqrt(i+1))        
            
        return sum1 - prod + 1 
    
    
    
    
    

    def _getDeJongDynamicFitness(self,gen):                
        currentStep = Global().getStep()
        modifiers = array('f', [0, 0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2])
        
        
        mod= (currentStep // 1000)% len(modifiers)# co 1000 krokow robimy adaptacje fitn         
                    
        result = 0
        for el in gen:
            result += (el-modifiers[mod]) * (el-modifiers[mod])
        return result


#    def _getRosenbrockFitness(self,gen):
#        assert Parameters.genotypeLength == 2
#        x = gen[0]
#        y = gen[1]
#        return math.pow(1-x, 2) + 100*pow(y - x*x, 2)

    # f(x)=0, x[i]=1
    def _getRosenbrockFitness(self,gen):        
        result = 0
        for i in xrange(len(gen)-1):
            result += 100 * (gen[i+1]- gen[i]*gen[i])*(gen[i+1]- gen[i]*gen[i])  +(1-gen[i])*(1-gen[i])
        return result
            

    
    def _getAckleyFitness(self,gen):
        genSum = 0
        cos_sum = 0
        val = 2*math.pi
        for x_i in gen:
            genSum += x_i * x_i
            cos_sum += math.cos(val*x_i)
        return -20*math.exp(-0.2*math.sqrt(genSum/Parameters.genotypeLength))-math.exp(cos_sum/Parameters.genotypeLength)+20+math.exp(1)

    def cosinus(self, specimen2):
        vec1, vec2 = self.getGenotype(), specimen2.getGenotype()
        sumxy = float(sum([vec1[key] * vec2[key] for key in range(len(vec1))]))
        if sumxy == 0.0:
            return 0.0
        sumx = float(sum([vec1[key] ** 2 for key in range(len(vec1))]))
        sumy = float(sum([vec2[key] ** 2 for key in range(len(vec1))]))
        return sumxy / (math.sqrt(sumx) * math.sqrt(sumy))

    def wantToReproduce(self):
        if self._energy >= self._reproductionMinEnergy:
            if self._energy - Parameters.initEnergy / 2 > 0:
                return True
        return False
    
    def wantToMigrate(self):
        if self._rand.random() <= Parameters.migrationProbability:
            return True
        return False
    
    def getEnergy(self):
        return self._energy
    
    def setEnergy(self, energy):
        self._energy = energy
    
    def setAfterReproductionEnergy(self):
        self._energy -= Parameters.initEnergy/2
        
    def rollbackReproductionEnergy(self):
        self._energy += Parameters.initEnergy/2
        
    def getGenotype(self):
        return self._genotype

    def getWonFightsCount(self):
        return self._won

    def getLostFightsCount(self):
        return self._lost
    
    def setNewGenotype(self, gen1, gen2, energy1, energy2, parentsFightsWon, parentsFightsLost):
        gen=getattr(self, "_cross"+Parameters.crossover)(gen1,gen2)
        islandEnergies = [child.getEnergy() for child in self.getParent().getChildren()]
        meanIslandEnergy = mean(islandEnergies)
        #meanIslandEnergy = mean([energy/(max(islandEnergies)/max(gen)) for energy in islandEnergies])
        parentsEnergies = [energy1, energy2]
        meanParentsEnergy = mean(parentsEnergies)
        #meanParentsEnergy = mean([energy/(max(parentsEnergies)/max(gen)) for energy in parentsEnergies])
        self._genotype=Mutation().mutate(gen, self._rand, meanIslandEnergy, meanParentsEnergy, parentsFightsWon, parentsFightsLost)
        self._recalculateFitness()
        
    def _crossSinglePoint(self,gen1,gen2):
        newGenotype = []
        part = self._rand.randint(0, Parameters.genotypeLength-1)
        for i in xrange(part):
            newGenotype += [gen1[i]]
        for i in xrange(part, Parameters.genotypeLength):
            newGenotype += [gen2[i]]
        return newGenotype
    
    def _crossSinglePointPermutation(self,gen1,gen2):                        
        newGenotype = []
        
        g1 = list(gen1)
        g2 = list(gen2)
        part = self._rand.randint(0, Parameters.genotypeLength-1)
        for i in xrange(part):
            newGenotype += [g1[i]]
        
        for i in newGenotype:
            g2.remove(i)
        
        for i in g2:
            newGenotype += [i]
                                          
        return newGenotype




    
    def fight(self, otherAgent):
        #myFitness = self.getFitness()
        myFitness=self._fitness
        otherAgentFitness = otherAgent.getFitness()
        if myFitness <= otherAgentFitness:
            self._energy += Parameters.fightEnergyWin
            otherAgent._energy += Parameters.fightEnergyLoose
            self._lost += 1
            self._checkIfKill(otherAgent, self)
        else:
            otherAgent._energy += Parameters.fightEnergyWin
            self._energy += Parameters.fightEnergyLoose
            self._won += 1
            self._checkIfKill(self, otherAgent)
        if Parameters.memetics!='None':
            mm = globals()[Parameters.memetizationManager]()
            if mm.shouldMemetize(self.getGenotype()):
                fitnessBefore = self.getFitness()
                genotypeBefore = self.getGenotype()
                self.memetize()
                fitnessAfter = self.getFitness()
                mm.collectInformation(genotypeBefore, - fitnessAfter + fitnessBefore)
            
    def memetize(self):
        mut = globals()[Parameters.memeticMutation+'Mutation']
        #self._genotype = LamarckMutation().mutate(self._genotype, self._rand, self._parent.getBestGenotype(), getattr(self, "_get"+Parameters.function+"Fitness"))
        if Parameters.memetics=='Lamarck':
            self._fitnessCalls += 1
            if(Global().getStep() % Parameters.statsCollectFreq == 0):
                fitnessCallsOfile = open('reproduceCountLamarck.txt', 'a')
                fitnessCallsOfile.write(str(Global().getStep())+";"+str(self._fitnessCalls)+"\n")
                fitnessCallsOfile.close()
            self._genotype = mut().mutate(self._genotype, self._rand, self._parent.getBestGenotype(), getattr(self, "_get"+Parameters.function+"Fitness"))
            self._recalculateFitness()
        elif Parameters.memetics=='Baldwin':
            genotype = mut().mutate(self._genotype, self._rand, self._parent.getBestGenotype(), getattr(self, "_get"+Parameters.function+"Fitness"))
            self._fitness = getattr(self, "_get"+Parameters.function+"Fitness")(genotype)
            self._updated=Global().getStep()            
    
    def memetizeSGA(self,best):        
        mut = globals()[Parameters.memeticMutation+'Mutation']
        #self._genotype = LamarckMutation().mutate(self._genotype, self._rand, best, getattr(self, "_get"+Parameters.function+"Fitness"))
        if Parameters.memetics=='Lamarck':
            self._genotype = mut().mutate(self._genotype, self._rand, best, getattr(self, "_get"+Parameters.function+"Fitness"))
            self._recalculateFitness()
        elif Parameters.memetics=='Lamarck':
            genotype = mut().mutate(self._genotype, self._rand, best, getattr(self, "_get"+Parameters.function+"Fitness"))
            self._fitness = getattr(self, "_get"+Parameters.function+"Fitness")(genotype)
            self._updated=Global().getStep()            


        
    def _checkIfKill(self, looser, winner):
        if looser._energy <= Parameters.dieEnergy:
            winnerEnergy = winner.getEnergy()
            winnerEnergy -= (Parameters.dieEnergy - looser._energy)
            winner.setEnergy(winnerEnergy)
            looser.kill()
    
    def movePossibilities(self):
        return self.getEnv().getFreeFields(self)
    
    def wantToMeet(self):
        value = self._rand.random()
        if value <= Parameters.meetingProbability:
            return True
        return False
