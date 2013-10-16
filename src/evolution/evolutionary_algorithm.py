from implementation.Parameters import Parameters
from random import Random, choice
from implementation.Specimen import Specimen

class EvolutionaryAlgorithm(object):
    
    def __init__(self):
        self._specimens = []
        self._rand = Random()
        for i in xrange(Parameters.agentCount):
            self._specimens.append(Specimen(None, None))
        self._global_min = 1000
  
    ############################# evolutionary algorithm part ###########################
    
    def _eval(self):
        self._fitnesses = []
        for specimen in self._specimens:
            self._fitnesses.append(specimen.getFitness())
        self._global_min=min(self._global_min, min(self._fitnesses))
        #print self._global_min
    
    def _chooseBest(self):
        tmp = {}
        for i in xrange(len(self._specimens)):
            tmp[self._fitnesses[i]] = self._specimens[i]
        keys = tmp.keys()
        keys.sort()
        sortedVal = [tmp[key] for key in keys]
        return sortedVal[:Parameters.bestNumber]
    
    def _selection(self):
        winners = []
        tmp = []
        for i in xrange(len(self._specimens)):
            tmp.append([self._specimens[i], self._fitnesses[i]])
        maxVal = len(tmp)-1
        for i in xrange(Parameters.matingPoolSize):
            index1 = self._rand.randint(0, maxVal)
            speciman1 = tmp[index1] 
            index2 = self._rand.randint(0, maxVal)
            speciman2 = tmp[index2] 
            if speciman1[1] <= speciman2[1]:
                winners.append(speciman1)
            else:
                winners.append(speciman2)
        return winners
    
    def _get_next(self, matingPool):
        maxVal = len(matingPool)-1
        while(True):
            value = self._rand.randint(0, maxVal)
            yield matingPool[value][0]
                
    def _create_new_population(self, matingPool, best):
        new_population = []
        get_next = self._get_next(matingPool)
        for i in xrange(Parameters.agentCount-len(best)):
            parent1 = get_next.next()
            parent2 = get_next.next()
            new_speciman = Specimen(None, None)
            new_speciman.setNewGenotype(parent1.getGenotype(), parent2.getGenotype())
            if Parameters.memetics!='None':                
                new_speciman.memetizeSGA(self._bestGen())
            new_population.append(new_speciman)
        new_population += best
        return new_population

    def _bestGen(self):
        best=None
        for i in range(len(self._fitnesses)):
            if best==None or self._fitnesses[i]<=self._fitnesses[best]:
                best=i
        retgen=self._specimens[i].getGenotype()
        return retgen

    
    def doStep(self):
        self._eval()
        best = self._chooseBest()
        matingPool = self._selection()
        new_population = self._create_new_population(matingPool, best)
        self._specimens = new_population
        
    #################### statistics section #####################################
     
    def getCount(self):
        return len(self._specimens) 
    
    def getMin(self):
        result = 1000
        for fitness in self._fitnesses:
            if result>fitness:
                result = fitness
        return result
    
    def getMax(self):
        result = 0
        for fitness in self._fitnesses:
            if result<fitness:
                result = fitness
        return result
    
    def getGenotypes(self):
        result = []
        for child in self._specimens:
            result.append(child.getGenotype())
        return result
    
    def getFitnesses(self):
        return self._fitnesses

    def getDescendants(self, parent=True):
        return [self] if parent else []

    def getSpecimensWantToMigrate(self):
        return [specimen for specimen in self._specimens if specimen.wantToMigrate()]

    def getRandomSpecimens(self, count):
        ids = range(len(self._specimens))
        specimens_ids = []
        for i in range(count):
            el = choice(ids)
            specimens_ids.append(el)
            ids.remove(el)
        return [self._specimens[sid] for sid in specimens_ids]
        

    def addSpecimens(self, *specimens):
        for specimen in specimens:
            self._specimens.append(specimen)
    
    def removeSpecimens(self, *specimens):
        for specimen in specimens:
            self._specimens.remove(specimen)
    

if __name__=="__main__":
    alg = EvolutionaryAlgorithm()
    for i in xrange(Parameters.simSteps):
        alg.doStep()
    