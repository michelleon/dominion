from core.card import KingdomCard
from core.card import CardType


class GardensCard(KingdomCard):
    """
    Worth 1 VP for every 10 cards you have (rounded down).
    """
    types = (CardType.VICTORY,)
    base_cost = 4
    
    @classmethod
    def victory_points(cls, player, game_state):
        deck_size = len(game_state.get_deck(player))
        return (deck_size // 10)
