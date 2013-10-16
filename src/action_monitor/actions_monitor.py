class ActionMonitor(object):
    
    def printAgregatedValue(self):
        pass
        
    '''stats is a dictionary
    for meeting actions it has keys:
     - fail - bool
     - wantMeet - bool
     - agents - list of two meeting agents
     - action - "reproduce", or "fight"
    they can be None 
    '''
    def actualStats(self, stats):
        pass
    
    def monitoredAgentClasses(self):
        return []