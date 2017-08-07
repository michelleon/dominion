from core.card import Card
from core.card import CardType
from core.game_state import CURRENT_PLAYER
from base_set.instructions import DrawCardsInstruction


class Smithy(Card):
	card_types = (CardType.ACTION,)
	base_treasure_cost = 4
	instructions = (DrawCardsInstruction(number_to_draw=3, target_player=CURRENT_PLAYER),)
