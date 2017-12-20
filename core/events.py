"""
Events represent any change to the game state. All changes to game state should
be represented by events so that if one was given a chronological list of events
they could reconstruct the game.
"""
from collections import namedtuple
import enum


class CardEventType(enum.Enum):
    PLAY = 0
    GAIN = 1
    BUY = 2
    DISCARD = 3
    SET_ASIDE = 4
    TRASH = 5
    DRAW = 6
    REVEAL = 7
    LOOK_AT = 8
    SHUFFLE = 9
    MOVE = 10

CardMoveEvent = namedtuple('CardMoveEvent', [
    'cards',
    'from_location',
    'from_position',
    'to_location',
    'to_position',
    'type',
])
CardMoveEvent.__doc__ = """
Represents an event that happens to a card. There are two groups of card events, events that
move a card or cards from one location to another, and events that reveal that card to one
or more players.

Parameters:
    cards (list of `Card`): One or more cards. The subjects of the event.
    from_location (`Location`): Location the target cards are in.
    from_position (optional, `StackPosition`): Position of the cards within the location.
        This is optional, it only matters if the cards are ordered within a location.
    to_location (optional, `Location`): Location to move the cards to. Not all events cause cards
        to move locations so this is optional.
    to_position (optional, `StackPosition`): Position in the to_location for the cards to go.
    type (`CardEventType`): The type of the event. Different event types may trigger other things
        to happen.
"""

ShuffleEvent = namedtuple('ShuffleEvent', ['location'])


class CardKnowledgeEventType(enum.Enum):
    REVEAL = 0
    LOOK = 1


CardKnowledgeEvent = namedtuple('CardKnowledgeEvent', [
    'players',
    'cards',
    'from_location',
    'from_position',
    'number',
    'type',
])
CardKnowledgeEvent.__doc__ = """
An event where no game state was updated, but some state was revealed to players.

Parameters:
    players (list of `str`): List of the player names of the players who were given the knowledge.
    cards (list of `Card`): List of cards the players saw.
    from_location (`Location`): Location the cards are located in.
    from_position (`StackPosition`): Position of the cards in the location.
    number (`int`): Number of cards revealed
    type (`KnowledgeEventType`): Type of the event. Some cards may be triggered depending on the
        way the knowledge event is defined.
"""


class CounterEventType(enum.Enum):
    # The counter was updated to a specific value.
    SET = 0
    # The counter was incremented/decremented by a value.
    UPDATE = 1


CounterEvent = namedtuple('CounterEvent', [
    'counter_id',
    'type',
    'value',
])
CounterEvent.__doc__ = """
Represents a change to a game counter.

Parameters:
    counter_id (`CounterId`): CounterId of the counter being updated.
    type (`CounterEventType`): Type of the counter event.
    value (int): Value the counter was set to or adjusted by. This can be negative to decrement the
        counter.
"""

EVENT_CLASSES = (
    CardMoveEvent,
    CardKnowledgeEvent,
    ShuffleEvent,
    CounterEvent,
)
