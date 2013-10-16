from action_monitor.actions_monitor import ActionMonitor
from implementation.Specimen import Specimen

class SimilarityReproductionMonitor(ActionMonitor):   
    
    def __init__(self):
        ActionMonitor.__init__(self)
        self._cosinusesHist = {}
        
        self.ranges = []
        start, step = 0.0, 0.05
        while start < 1.0:
            label = "%.2f - %.2f" % (start, start + step)
            self.ranges.append((start, start + step, label))
            self._cosinusesHist[label] = 0
            start += step
    
    def monitoredAgentClasses(self):
        return [Specimen]
    
    def printAgregatedValue(self):
        print "SimilarityReproductionMonitor:"
        print 'Similarity (cos): reproductions'
        for item in sorted(self._cosinusesHist, 
                           key=lambda key: float(key.split('-')[0].strip()),
                           reverse=True):
            print '%s: %d' % (item, self._cosinusesHist[item])
        
    def actualStats(self, stats):
        for stat in stats:
            if not stat["wantMeet"] or stat["duringMeeting"] or stat["noAgentToMeet"]:
                continue
            if stat["action"] == "reproduce":
                for start, end, label in self.ranges:
                    if start < stat["agentsSimilarity"] <= end:
                        self._cosinusesHist[label] += 1
                        break
