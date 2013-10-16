from action.Action import Action
class ChangeAgentEnergyAction(Action):

    def __init__(self, agent):
        self._agent = agent
        self._agent.setAgentMeeting(True)

        
    def doAction(self):
        self._agent.setAfterReproductionEnergy()

        
    def rollback(self, index):
        self._agent.rollbackReproductionEnergy()