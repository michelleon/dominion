from core.card import KingdomCard
from core.card import CardType
from core.decision import Decision
from core.locations import Location
from core.locations import LocationName
from core.counters import CounterId
from core.counters import CounterName
from base_set.cards import CopperCard


class MoneyLenderDecision(Decision):
    def __init__(self, game_state):
        hand = game_state.get_location(
            Location(game_state.get_current_player_name(), LocationName.HAND)
        )
        self.options = []
        if CopperCard in hand:
            self.options = [CopperCard]
        self.min = 0
        self.max = 1


class MoneyLenderCard(KingdomCard):
    types = (CardType.ACTION,)
    base_cost = 4

    @classmethod
    def play(cls, game_state):
        decision = MoneyLenderDecision(game_state)
        agent = game_state.get_agent(game_state.get_current_player_name())
        # No coppers to trash
        if decision.there_is_no_choice():
            return
        choice = agent.make_decision(decision)
        if choice == [CopperCard]:
            game_state.trash(CopperCard)
            game_state.update_counter(counter_id=CounterId(None, CounterName.COINS), delta=3)
