from collections import namedtuple
import enum


class CounterName(enum.Enum):
    COINS = 0
    ACTIONS = 1
    BUYS = 2


# Complete list of global counter names, all others are local.
GLOBAL_COUNTERS = set((
	CounterName.COINS,
	CounterName.ACTIONS,
	CounterName.BUYS,
))


CounterId = namedtuple('CounterId', ['player', 'name'])
CounterId.__doc__ = """
An identifier for a game state counter. Counters can be global or local to one player.
Global counters will have a CounterId with None for the player.

Parameters:
    player (optional, str): Name of the player that owns the counter or None if it's global.
    name (`CounterName`): Name of the counter.
"""
