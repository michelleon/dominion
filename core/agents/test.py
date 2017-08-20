from core.agents.base import BaseAgent
from core.decision import PlayTreasureDecision


class TestAgent(BaseAgent):
    """
    An agent that plays mostly randomly. It will always play all it's treasures and
    always play at least one action if it can. It will all other decisions at random.
    """
    def make_decision(self, decision, known_state=None):
        if isinstance(decision, PlayTreasureDecision):
            # Play all treasures
            choice = decision.options
            return choice
        choice =  decision.choose_random()
        return choice

