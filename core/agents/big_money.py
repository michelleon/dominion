import random

from base_set.cards import SmithyCard
from base_set.cards import ProvinceCard
from core.agents.base import BaseAgent
from core.decision import PlayTreasureDecision
from core.decision import BuyDecision
from core.decision import PlayActionDecision


class DumbMoneyAgent(BaseAgent):
    """
    An agent that just buys money until it can buy Provinces. It follow these rules:

    - If I can buy Province I buy province
    - If I cannot buy Province I buy most expensive treasure except Copper
    - Never buy Copper
    - If I have to make a play action decision choose one randomly
    """
    def make_decision(self, decision, known_state=None):
        if isinstance(decision, PlayTreasureDecision):
            choice = decision.options
        elif isinstance(decision, BuyDecision):
            if ProvinceCard in decision.options:
                choice = [ProvinceCard]
            else:
                max_treasure = max(decision.options, key=lambda x: getattr(x, 'base_treasure_value', 0))
                if max_treasure and getattr(max_treasure, 'base_treasure_value', 0) > 1:
                    choice = [max_treasure]
                else:
                    choice = []
        elif isinstance(decision, PlayActionDecision):
            choice = [random.choice(decision.options)]
        return choice


class SimpleBmSmithyAgent(BaseAgent):
    """
    An agent that opens with a Smithy and then buys Province when it can, otherwise the best
    treasure available except Copper. Always plays Smithy from its hand when possible.
    """
    def __init__(self, *args, **kwargs):
        super(SimpleBmSmithyAgent, self).__init__(*args, **kwargs)
        self._bought_a_smithy = False

    def make_decision(self, decision, known_state=None):
        if isinstance(decision, PlayTreasureDecision):
            choice = decision.options
        elif isinstance(decision, BuyDecision):
            if ProvinceCard in decision.options:
                choice = [ProvinceCard]
            elif SmithyCard in decision.options and not self._bought_a_smithy:
                self._bought_a_smithy = True
                choice = [SmithyCard]
            else:
                max_treasure = max(
                    decision.options,
                    key=lambda x: getattr(x, 'base_treasure_value', 0)
                )
                if max_treasure and getattr(max_treasure, 'base_treasure_value', 0) > 1:
                    choice = [max_treasure]
                else:
                    choice = []
        elif isinstance(decision, PlayActionDecision):
            choice = decision.options[:1]
        return choice
