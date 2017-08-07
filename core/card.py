from enum import Enum

DEFAULT_STARTING_PILE_SIZE = 10


class CardType(Enum):
    ACTION = 1
    TREASURE = 2
    VICTORY = 3
    CURSE = 4
    ATTACK = 5
    REACTION = 6


class Card(object):
    card_types = ()
    base_treasure_cost = 0
    instructions = ()

    @staticmethod
    def get_starting_pile_size(num_players):
        """
        Return the number of this card that should start in the supply given that num_players
        are in the game.
        """
        return DEFAULT_STARTING_PILE_SIZE
