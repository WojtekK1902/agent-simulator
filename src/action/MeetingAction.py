from action.ComplexAction import ComplexAction
from action.fight.FightAction import FightAction
from action.fight.KillAgentAction import KillAgentAction
from action.reproduce.ChangeAgentEnergyAction import ChangeAgentEnergyAction
from action.reproduce.CreateAgentAction import CreateAgentAction

class MeetingAction(ComplexAction):

    def __init__(self, agent, simLogic):
        ComplexAction.__init__(self)
        
        self._stats["agent"] = agent
        
        if not agent.wantToMeet():
            self._stats["wantMeet"] = False
            return
        
        self._stats["wantMeet"] = True
        
        self._simLogic = simLogic
        
        self._stats["duringMeeting"] = False
        
        if agent.isDuringMeeting():
            self._stats["duringMeeting"] = True
            self._stats["duringMeetingAgent"] = agent
            return
        
        meetingAgent = agent.meetAgent()
        
        self._stats["noAgentToMeet"] = False
        
        self._stats["agentsSimilarity"] = None
        
        if meetingAgent is None:
            self._stats["noAgentToMeet"] = True
            return
        
        if meetingAgent.isDuringMeeting():
            return
        
        if agent.wantToReproduce() is None:
            return
        
        agent.setAgentMeeting(True)
        meetingAgent.setAgentMeeting(True)
        
        self._stats["agents"] = [agent, meetingAgent]
        
        if agent.wantToReproduce() and meetingAgent.wantToReproduce():
            self._stats["action"] = "reproduce"
            self._stats["agentsSimilarity"] = agent.cosinus(meetingAgent)
            self.reproduce(agent, meetingAgent)
        else:
            self._stats["action"] = "fight"
            self.fight(agent, meetingAgent)
        self._changeAddittionalInfo(agent,1)
            
    def reproduce(self, agent, meetingAgent):
        self.addAction(ChangeAgentEnergyAction(agent))
        self.addAction(ChangeAgentEnergyAction(meetingAgent))
        self.addAction(CreateAgentAction(agent, meetingAgent, self._simLogic))
        
    def fight(self, agent, meetingAgent):
        self.addAction(FightAction(agent,meetingAgent))
        self.addAction(KillAgentAction(agent, self._simLogic))
        self.addAction(KillAgentAction(meetingAgent, self._simLogic))
    
    def _changeAddittionalInfo(self, agent, value):
        val = agent.getParent().getAddittionalInfo("meeting")
        if val is None:
            val = 0
        val += value
        agent.getParent().setAddittionalInfo("meeting", val)
