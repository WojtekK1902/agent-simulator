from action.MeetingAction import MeetingAction
from action.MoveAction import MoveAction
from action.migration.MigrationAction import MigrationAction
from implementation.HerdAgent import HerdAgent
from implementation.Parameters import Parameters
from simulation.SimLogic import SimLogic
from simulation.Global import Global

class GeneticSimLogic(SimLogic):
    
    def __init__(self):
        super(GeneticSimLogic, self).__init__()
        
    def getAgentStatsClass(self):
        return HerdAgent
        
    def runSimulation(self, simSteps):
        try:
            self._count = 0
            g = Global()
            while (simSteps is None or self._count < simSteps) and (self._stepsMonitor is None or self._stepsMonitor.getAgentsSteps() < Parameters.agentSteps):
                SimLogic.timestamp = self._count
                g.nextStep()
                self.doStep()
                self._count += 1
                #sleep(1)
        except KeyboardInterrupt:
            for key in self._visualisationListeners.keys():
                for listener in self._visualisationListeners.get(key):
                    listener.show()
            if simSteps is None:
                print "simSteps: "+str(self._count)
            return
        for key in self._visualisationListeners.keys():
                for listener in self._visualisationListeners.get(key):
                    listener.show()
        if simSteps is None:
            print "simSteps: "+str(self._count)

    def _decisionPhase(self):
        for rootAgent in self._agents:
            for agent in rootAgent.getDescendants(parent=True):
                self._actionManager.addAction(MoveAction(agent))
            for agent in rootAgent.getDescendants(parent=True):
                self._actionManager.addAction(MeetingAction(agent, self))
            self._actionManager.addAction(MigrationAction(rootAgent, self))

    def _executivePhase(self):
        self._actionManager.doActions()
        for rootAgent in self._agents:
            for agent in rootAgent.getDescendants(parent=True):
                agent.setAgentMeeting(False)

    def _visualise(self):
        if Parameters.drawCharts == False and Parameters.showOutput == False:
            return
        visualisationData = {}
        for rootAgent in self._agents:
            for agent in rootAgent.getDescendants(parent=True):
                list = visualisationData.get(agent.__class__, [])
                agentAttr = []
                for attr in agent.visualise:
                    method = "get" + attr[0].upper() + attr[1:]
                    agentAttr.append(getattr(agent, method)())
                list.append(agentAttr)
                visualisationData[agent.__class__] = list
        for key in self._visualisationListeners.keys():
            data = visualisationData.get(key, [])
            for listener in self._visualisationListeners.get(key):
                listener.visualise(data)

