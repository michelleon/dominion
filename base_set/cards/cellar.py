from core.card import CardType
from core.card import KingdomCard
from core.counters import CounterId
from core.counters import CounterName
from core.decision import Decision
from core.locations import Location
from core.locations import LocationName


class CellarDecision(Decision):
    def __init__(self, game_state):
        player = game_state.get_current_player_name()
        cards = list(game_state.get_location(Location(player, LocationName.HAND)))
        self.options = cards
        self.min = 0
        self.max = min(len(cards), 4)


class CellarCard(KingdomCard):
    types = (CardType.ACTION,)
    base_cost = 2

    @classmethod
    def play(cls, game_state):
        """
        Discard any number of cards, then draw that many
        +1 action
        """
        decision = CellarDecision(game_state)
        agent = game_state.get_agent(game_state.get_current_player_name())
        chosen_cards = agent.make_decision(decision)
        assert decision.is_valid(chosen_cards)

        game_state.discard(chosen_cards)
        game_state.draw(len(chosen_cards))
        game_state.update_counter(counter_id=CounterId(None, CounterName.ACTIONS), delta=1)
