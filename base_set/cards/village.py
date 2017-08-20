from core.card import CardType
from core.card import KingdomCard
from core.counters import CounterId
from core.counters import CounterName


class VillageCard(KingdomCard):
    types = (CardType.ACTION,)
    base_cost = 3

    @classmethod
    def play(cls, game_state):
        game_state.draw(1)
        game_state.update_counter(counter_id=CounterId(None, CounterName.ACTIONS), delta=2) 
