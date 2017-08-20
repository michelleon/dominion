from core.card import Card
from core.card import CardType


class CurseCard(Card):
    types = (CardType.CURSE,)
    base_cost = 0
    vp = -1
