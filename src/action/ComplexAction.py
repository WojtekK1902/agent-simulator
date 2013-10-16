from action.Action import Action

class ComplexAction(Action):

    def __init__(self):
        self._actionIndex = 0
        self._actions = []
        self._stats = {}
        self._stats["fail"] = False

    def addAction(self, action):
        self._actions.append(action)

    def doAction(self):
        #if len(self._actions) == 0:
        #    raise SystemError("Action is on the bottom of the hierarchy.")
        try:
            for action in self._actions:
                action.doAction()
                self._actionIndex += 1
        except RuntimeError:
            self.rollback(self._actionIndex)

    def rollback(self, index):
        self._stats["fail"] = True
        if index == -1:
            index = len(self._actions) - 1
        while index >= 0:
            self._actions[index].rollback(-1)
            index -= 1
        raise RuntimeError()
    
    def getStats(self):
        return self._stats
