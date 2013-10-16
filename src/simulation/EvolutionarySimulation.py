from simulation.Simulation import Simulation
from simulation.EvolutionarySimLogic import EvolutionarySimLogic
from evolution.evolutionary_algorithm import EvolutionaryAlgorithm
from implementation.Parameters import Parameters

class EvolutionarySimulation(Simulation):
    def __init__(self):
        super(EvolutionarySimulation, self).__init__()
        
        self._simLogic = EvolutionarySimLogic()
        for i in xrange(Parameters.herdAgentsCount):
            herdAgent = EvolutionaryAlgorithm()
            self._simLogic.addAgents(herdAgent)

if __name__ == '__main__':
    EvolutionarySimulation()
