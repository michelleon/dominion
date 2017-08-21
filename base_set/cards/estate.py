from core.card import Card
from core.card import CardType


class EstateCard(Card):
    types = (CardType.VICTORY,)
    base_cost = 2
    vp = 1
