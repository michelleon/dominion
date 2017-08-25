from core.card import KingdomCard
from core.card import CardType
from core.decision import Decision
from core.locations import Location
from core.locations import LocationName
from core.counters import CounterId
from core.counters import CounterName
from base_set.cards import CopperCard


class WorkshopDecision(Decision):
    def __init__(self, game_state):
        supply = game_state.get_location(Location(None, LocationName.SUPPLY))
        options = []
        for card, count in supply.distribution.cards_to_counts().items():
            if count > 0 and card.cost(game_state) <= 4:
                options.append(card)
        self.options = options
        # Player must gain something if possible
        self.min = 1 if options else 0
        self.max = 1


class WorkshopCard(KingdomCard):
    """
    Gain a card costing up to 4.
    """
    types = (CardType.ACTION,)
    base_cost = 3

    @classmethod
    def play(cls, game_state):
        decision = WorkshopDecision(game_state)
        agent = game_state.get_agent(game_state.get_current_player_name())
        if decision.there_is_no_choice():
            return
        choice = agent.make_decision(decision)
        assert decision.is_valid(choice)
        game_state.gain(choice[0])
