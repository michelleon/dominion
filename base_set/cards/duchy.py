from core.card import Card
from core.card import CardType


class DuchyCard(Card):
    types = (CardType.VICTORY,)
    base_cost = 5
    vp = 3
