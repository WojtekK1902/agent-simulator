from simulation.Simulation import Simulation
from simulation.GeneticSimLogic import GeneticSimLogic
from environment.Environment2D import Environment2D
from implementation.HerdAgent import HerdAgent
from implementation.Specimen import Specimen
from implementation.Parameters import Parameters
from implementation.Visualisation import Visualisation

class GeneticSimulation(Simulation):
    def __init__(self):
        super(GeneticSimulation, self).__init__()
        
        self._simLogic = GeneticSimLogic()
        env = Environment2D('env2d', 3, 3)
        fieldSize = Parameters.fieldSize
        for i in xrange(Parameters.herdAgentsCount):
            herdAgent = HerdAgent(env, Environment2D('env2d_' + str(i), fieldSize, fieldSize))
            for j in xrange(Parameters.agentCount):
                specimen = Specimen(None, herdAgent.getChildrenEnv())
                herdAgent.addAgents(specimen)
            self._simLogic.addAgents(herdAgent)
        self._simLogic.addVisualisationListener(Visualisation(), HerdAgent)

if __name__ == '__main__':
    GeneticSimulation()
