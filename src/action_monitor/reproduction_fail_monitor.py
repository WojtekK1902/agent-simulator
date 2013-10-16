from action_monitor.actions_monitor import ActionMonitor
from implementation.Specimen import Specimen


class ReproductionFailMonitor(ActionMonitor):   
    
    def __init__(self):
        ActionMonitor.__init__(self)
        self._reproductionsCount = 0.0
        self._fightsCount = 0.0
        self._count = 0.0
        self._failReproductions = 0.0
        self._failFights = 0.0
        self._dontHavePartnerCount = 0.0
        self._partnerDuringMeeting = 0.0
        self._maxReproductionsCount = None
        self._minReproductionsCount = None
        self._maxFightsCount = None
        self._minFightsCount = None
        self._meetingsCount = 0.0
    
    def monitoredAgentClasses(self):
        return [Specimen]
    
    def printAgregatedValue(self):
        print "ReproductionFailMonitor:"
        print " - Max reproductions count: "+str(self._maxReproductionsCount)
        print " - Min reproductions count: "+str(self._minReproductionsCount)
        print " - Avg reproductions count: "+str(self._reproductionsCount/self._count)
        print " - Avg failed reproductions count: "+str(self._failReproductions/self._count)
        print " - Max fights count: "+str(self._maxFightsCount)
        print " - Min fights count: "+str(self._minFightsCount)
        print " - Avg fights count: "+str(self._fightsCount/self._count)
        print " - Avg failed fights count: "+str(self._failFights/self._count)
        print " - Avg agents which dont have partner: "+str(self._dontHavePartnerCount/self._count)
        print " - Avg agents which are during meeting: "+str(self._partnerDuringMeeting/self._count)
        print " - Avg (sucessfull) meetings count: "+str(self._meetingsCount/self._count)
        
        
    def actualStats(self, stats):
        reproductionsCount = 0.0
        fightsCount = 0.0
        self._count += 1
        for stat in stats:
            if not stat["wantMeet"]:
                continue
            if stat["duringMeeting"]:
                self._partnerDuringMeeting += 1
                continue
            if stat["noAgentToMeet"]:
                self._dontHavePartnerCount += 1
                continue
            self._meetingsCount += 1
            if stat["action"] == "reproduce":
                reproductionsCount += 1
                if stat["fail"]:
                    self._failReproductions += 1
            else:
                fightsCount += 1
                if stat["fail"]:
                    self._failFights += 1
        
        self._reproductionsCount += reproductionsCount
        self._fightsCount += fightsCount
        
        if self._maxReproductionsCount is None:
            if reproductionsCount > 0 or self._count > 1:
                self._maxReproductionsCount = reproductionsCount
                self._minReproductionsCount = reproductionsCount
        else:
            self._maxReproductionsCount = max(self._maxReproductionsCount, reproductionsCount)
            self._minReproductionsCount = min(self._minReproductionsCount, reproductionsCount)
            
        if self._maxFightsCount is None:
            if fightsCount > 0 or self._count > 1:
                self._maxFightsCount = fightsCount
                self._minFightsCount = fightsCount
        else:
            self._maxFightsCount = max(self._maxFightsCount, fightsCount)
            self._minFightsCount = min(self._minFightsCount, fightsCount)