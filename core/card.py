import enum

from core.counters import CounterId
from core.counters import CounterName


class CardType(enum.Enum):
	TREASURE = 0
	VICTORY = 1
	CURSE = 2
	ACTION = 3
	ATTACK = 4


# This is just so the Card classes display nicely in the shell
class Meta(type):
    def __repr__(cls):
        return cls.__name__


class Card(metaclass=Meta):
	# Tuple of `CardType`s
	types = tuple()
	# Cost to buy the card
	base_cost = 0
	# Amount of victory points the card grants a player if it's static.
	vp = 0

	classmethod
	def has_type(cls, card_type):
		return card_type in types

	@staticmethod
	def hasRandomizer():
		"""
		Return True if this card is included in the randomizer deck to choose what cards
		will be in a kingdom.
		"""
		return False

	@classmethod
	def cost(cls, game_state):
		"""
		Return the current cost of the card based given the game state.
		"""
		return  cls.base_cost

	@classmethod
	def victory_points(cls, player, game_state):
		"""
		Return the current number of victory points the card gives based on the gaem state.
		"""
		return cls.vp

	@classmethod
	def play(cls, game_state):
		raise NotImplementedError()


class KingdomCard(Card):
	@staticmethod
	def hasRandomizer():
		return True


class TreasureCard(Card):
	types = (CardType.TREASURE,)
	base_treasure_value = 0

	@classmethod
	def play(cls, game_state):
	    game_state.update_counter(
	    	counter_id=CounterId(None, CounterName.COINS), delta=cls.base_treasure_value
	    )


class HiddenCard(Card):
	pass