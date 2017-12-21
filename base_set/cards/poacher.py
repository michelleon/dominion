from core.card import KingdomCard
from core.card import CardType
from core.decision import Decision
from core.locations import Location
from core.locations import LocationName
from core.counters import CounterId
from core.counters import CounterName


class PoacherDecision(Decision):
    def __init__(self, game_state, cards_to_discard):
        player = game_state.get_current_player_name()
        hand = game_state.get_location(Location(player, LocationName.HAND))
        self.options = list(hand)
        self.min = min(len(self.options), cards_to_discard)
        self.max = self.min


class PoacherCard(KingdomCard):
    """
    +1 Card
    +1 Action
    +1 Coin

    Discard a card per empty Supply pile.
    """
    types = (CardType.ACTION,)
    base_cost = 4

    @classmethod
    def play(cls, game_state):
        game_state.draw(1)
        game_state.update_counter(counter_id=CounterId(None, CounterName.ACTIONS), delta=1)
        game_state.update_counter(counter_id=CounterId(None, CounterName.COINS), delta=1)
        supply = game_state.get_location(Location(None, LocationName.SUPPLY))
        cards_to_counts = supply.distribution.cards_to_counts()
        empty_supply_piles = list(cards_to_counts.values()).count(0)
        if empty_supply_piles == 0:
            return
        decision = PoacherDecision(game_state, empty_supply_piles)
        player = game_state.get_current_player_name()
        agent = game_state.get_agent(player)
        choice = agent.make_decision(decision)
        assert decision.is_valid(choice)
        game_state.discard(choice)
