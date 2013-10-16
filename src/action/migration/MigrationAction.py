from action.ComplexAction import ComplexAction
from action.migration.RemoveAgentAction import RemoveAgentAction
from action.migration.AddAgentAction import AddAgentAction

class MigrationAction(ComplexAction):
    
    def __init__(self, agent, simLogic):
        ComplexAction.__init__(self)
        self._simLogic = simLogic
        migrationDestination = agent.getMigrationDestination()
        if migrationDestination is None:
            return
        agentsToMigrate = self._getAgentsToMigrate(agent)
        for agentToMigrate in agentsToMigrate:
            self.addAction(RemoveAgentAction(agent, agentToMigrate))
            self.addAction(AddAgentAction(migrationDestination, agentToMigrate))
        
    def _getAgentsToMigrate(self, agent):
        agents = []
        for descendant in agent.getDescendants(parent=False):
            if descendant.wantToMigrate():
                agents.append(descendant)
        return agents
        