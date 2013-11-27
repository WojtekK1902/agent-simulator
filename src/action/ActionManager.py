from action import MeetingAction


class ActionManager(object):
    
    def __init__(self):
        self._actions = []
        self._k = 0
        
    def clear(self):
        self._actions = []

    def addAction(self, action):
        self._actions += [action]
    
    def doActions(self):
        for action in self._actions:
            try:
                action.doAction()
                self._k += 1
            except RuntimeError:
                    continue
        self._setMeetingActionStats()
        self.clear()

    def _setMeetingActionStats(self):
        self._meetingActionStats = []
        for action in self._actions:
            if type(action) == MeetingAction.MeetingAction:
                self._meetingActionStats.append(action.getStats())

    def getMeetingActionStats(self):
        return self._meetingActionStats