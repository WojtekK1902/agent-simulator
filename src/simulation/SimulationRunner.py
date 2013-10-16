from implementation.Parameters import Parameters
from simulation.GeneticSimulation import GeneticSimulation
from simulation.EvolutionarySimulation import EvolutionarySimulation

from monitor.AgentStepsCountMonitor import AgentStepsCountMonitor
from monitor.DiversityMonitor import DiversityMonitor
from monitor.CenterOfGravityMonitor import CenterOfGravityMonitor
from monitor.CenterOfGravityMoveMonitor import CenterOfGravityMoveMonitor
from monitor.DieAndReproductionMonitor import DieAndReproductionMonitor
from monitor.DistFromCoGMonitor import DistFromCoGMonitor
from monitor.MonitorsHolder import MonitorsHolder
from monitor.PopulationCountMonitor import PopulationCountMonitor
from monitor.ReadyToReproductionMonitor import ReadyToReproductionMonitor
from monitor.ResultMonitor import ResultMonitor
from monitor.SimStepsToMakeResultBetterMonitor import SimStepsToMakeResultBetterMonitor
from monitor.StatsCollector import StatsCollector
from monitor.ResultMonitor import ResultMonitor
from monitor.BestFitnessMonitor import BestFitnessMonitor
from action_monitor.action_monitors_holder import ActionMonitorsHolder
from action_monitor.reproduction_fail_monitor import ReproductionFailMonitor
from action_monitor.similarity_reproduction_monitor import SimilarityReproductionMonitor
from machine_learning.AQMemetizationManager import AQMemetizationManager
from machine_learning.NBMemetizationManager import NBMemetizationManager

class SimulationRunner(object):
    def __init__(self):
        if Parameters.changeSeries:
            number=Parameters.seriesNumber
            setattr(Parameters, Parameters.seriesParameterToChange, Parameters.seriesStart)
            print "Parametr:"+Parameters.seriesParameterToChange
            print "pocz wart:"+str(Parameters.seriesStart)
        else:
            number=1
            
        for s in xrange(number):
            if Parameters.changeSeries and s>0:
                setattr(Parameters, Parameters.seriesParameterToChange, getattr(Parameters,Parameters.seriesParameterToChange)+Parameters.seriesDelta)
                print "Parametr:"+Parameters.seriesParameterToChange
                print "nast wart:"+str(getattr(Parameters,Parameters.seriesParameterToChange))
                
                
            for i in xrange(Parameters.simulations):
                globals()[Parameters.memetizationManager]().clearInfo()
                if Parameters.printStatsGlobal:
                    print 'Simulation no. %d' % (i + 1)
                
                sim = globals()[Parameters.algorithm]()
                monitorsHolder = MonitorsHolder()
           
                stepsMonitor = None
                for monitor in Parameters.monitors:
                    monitorObj = globals()[monitor](sim._simLogic.getAgentStatsClass())
                    monitorsHolder.registerMonitor(monitorObj)
                    if monitor == "AgentStepsCountMonitor":
                        stepsMonitor = monitorObj
                        
                if Parameters.agentSteps is not None and stepsMonitor is None:
                    stepsMonitor = AgentStepsCountMonitor()
                    monitorsHolder.registerMonitor(stepsMonitor)
                if Parameters.agentSteps is None:
                    stepsMonitor = None
                    
                sim.setMonitorsHolder(monitorsHolder)
                
                actionMonitorsHolder = ActionMonitorsHolder()
                for monitor in Parameters.actionMonitors:
                    monitorObj = globals()[monitor]()
                    actionMonitorsHolder.registerMonitor(monitorObj)
                
                sim.setActionMonitorsHolder(actionMonitorsHolder)
                            
                sim.runSimulation(stepsMonitor)
                
                if Parameters.printStatsGlobal:
                    #monitorsHolder.printAgregatedValues()
                    print
                    #actionMonitorsHolder.printAgregatedValues()
                    print
                    print
