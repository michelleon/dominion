from core.card import Card
from core.card import CardType


class ProvinceCard(Card):
    types = (CardType.VICTORY,)
    base_cost = 8
    vp = 6
