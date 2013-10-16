from action.MeetingAction import MeetingAction
from action.MoveAction import MoveAction
from action.migration.MigrationAction import MigrationAction
from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from implementation.Specimen import Specimen
from random import Random, choice
from simulation.SimLogic import SimLogic
from simulation.Global import Global
from evolution.evolutionary_algorithm import EvolutionaryAlgorithm

class EvolutionarySimLogic(SimLogic):
    
    def __init__(self):
        super(EvolutionarySimLogic, self).__init__()

    def getAgentStatsClass(self):
        return EvolutionaryAlgorithm

    def runSimulation(self, simSteps):
        try:
            count = 0
            g = Global()
            for i in xrange(Parameters.simSteps):
                g.nextStep()
                for rootAgent in self._agents:
                    rootAgent.doStep()
                self._migration()
                self._setStats()
                count += 1
                
        except KeyboardInterrupt:
            if simSteps is None:
                print "simSteps: " + str(count)
            return
            
        if simSteps is None:
            print "simSteps: " + str(count)

    def _migration(self):
        """Migration may not look clear and obvious but we cannot
        change the number of specimens in each herd, because in this alg. it is const.
        """
        if len(self._agents) < 2:
            return
        for i in range(len(self._agents)):
            agent = self._agents[i]
            to_migrate = agent.getSpecimensWantToMigrate()
            if to_migrate:
                agents_ids = range(len(self._agents))
                agents_ids.remove(i)
                agent_to_id = choice(agents_ids)
                to_migrate2 = self._agents[agent_to_id].getRandomSpecimens(len(to_migrate))
                self._agents[i].removeSpecimens(*to_migrate)
                self._agents[agent_to_id].addSpecimens(*to_migrate)
                self._agents[agent_to_id].removeSpecimens(*to_migrate2)
                self._agents[i].addSpecimens(*to_migrate2)

    def addAgents(self, *agents):
        for agent in agents:
            self._agents += [agent]

    def _decisionPhase(self):
        pass
    
    def _executivePhase(self):
        pass
    
    def _visualise(self):
        pass
