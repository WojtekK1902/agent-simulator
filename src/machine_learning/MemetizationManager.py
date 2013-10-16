from random import Random
from simulation.Global import Global
from implementation.Parameters import *

class MemetizationManager(object):
    instances = {}
    def __new__(cls, *args, **kwargs):
        if MemetizationManager.instances.get(cls) is None:
            cls.__original_init__ = cls.__init__
            MemetizationManager.instances[cls] = object.__new__(cls, *args, **kwargs)
        elif cls.__init__ == cls.__original_init__:
            def nothing(*args, **kwargs):
                pass
            cls.__init__ = nothing
        return MemetizationManager.instances[cls]

    def __init__(self):
        self._info = [] #list of tuples: (genotype, fitnessDelta)
        self._rand = Random()
        self._learned = False

    def clearInfo(self):
        self._info = []

    def collectInformation(self, genotype, fitnessDelta):
        self._info.append((list(genotype), fitnessDelta))

    def shouldMemetize(self, genotype):
        if Global().getStep() < Parameters.simSteps / 3:
            return self._rand.randint(1,100)<=Parameters.memetizationProbability
        else:
            if self._learned == False:
                self.learn()
                self._learned = True
            return self.makeDecision(genotype)

    def learn(self):
        raise NotImplementedError()

    def makeDecision(self, genotype):
        raise NotImplementedError()
    
