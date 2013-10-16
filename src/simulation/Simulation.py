from implementation.Parameters import Parameters

class Simulation(object):
    def __init__(self):
        pass
    
    def runSimulation(self, stepsMonitor):
        self._simLogic.setAgentStepsMonitor(stepsMonitor)        
        self._simLogic.runSimulation(Parameters.simSteps)
        
    def setMonitorsHolder(self, holder):
        self._simLogic.setStatsListener(holder)

    def setActionMonitorsHolder(self, holder):
        self._simLogic.setActionsListener(holder)

    def movePossibilities(self):
        return self.getEnv().getFreeFields(self)