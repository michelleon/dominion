from core.card import CardType
from core.card import KingdomCard


class SmithyCard(KingdomCard):
    types = (CardType.ACTION,)
    base_cost = 4

    @classmethod
    def play(cls, game_state):
        game_state.draw(3)