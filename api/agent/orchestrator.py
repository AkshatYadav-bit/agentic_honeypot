from api.agent.policy import DialoguePolicy
from api.agent.personas import select_persona
from api.agent.responder import Responder


class AgentOrchestrator:
    def __init__(self):
        self.policy = DialoguePolicy()
        self.responder = Responder()

    def handle(self, session):
        decision = self.policy.decide(session)
        persona = select_persona(session)

        # Generate reply text
        reply = self.responder.generate(decision["next_action"], session)


        return {
            "reply": reply,
            "persona": persona.name,
            "decision": decision
        }
