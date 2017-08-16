from collections import namedtuple
import enum


class LocationName(enum.Enum):
    DRAW_PILE = 0
    HAND = 1
    IN_PLAY = 2
    DISCARD = 3
    SET_ASIDE = 4
    TRASH = 5
    SUPPLY = 6

# Complete list of global locations. ALl others are local.
GLOBAL_LOCATIONS = set((
    LocationName.SUPPLY,
    LocationName.TRASH,
))


Location = namedtuple('Location', ['player', 'name'])
Location.__doc__ = """
Location represents an area of the playing surface where cards can be stored. Locations can
be global, one for the whole game, or local, one per player. For example, the trash is a
global location while each players hand is a local location.

Parameters:
    player (optional, str): Name of the player that owns the location or None if it is a global.
    name (`LocationName`): Enum value for the name of the location.
"""
