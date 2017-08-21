from core.counters import CounterName
from core.events import CardEventType
from core.events import CardMoveEvent
from core.events import CounterEvent
from core.events import ShuffleEvent
from core.loggers.base import GameLogger
from core.locations import LocationName
from core.card_stack import StackPosition


class HumanReadableLogger(GameLogger):
    """
    Logger that prints each event in plain english.
    """
    def __init__(self):
        self._log = []

    def _card_move_event_to_str(self, event):
        s = '''
        {player} {type}s {cards} from {from_pos}{from_loc} to {to_pos}{to_loc}.
        '''.format(
            player=event.from_location.player or event.to_location.player,
            type=CardEventType(event.type).name,
            cards=', '.join([repr(card) for card in event.cards]),
            from_pos='' if event.from_position is None else StackPosition(event.from_position).name.lower() + ' of ',
            from_loc=LocationName(event.from_location.name).name,
            to_pos='' if event.to_position is None else StackPosition(event.to_position).name.lower() + ' of ',
            to_loc=LocationName(event.to_location.name).name,

        )
        s = s.strip()
        return s

    def _counter_event_to_str(self, event):
        s = '''
        {player}{number} {counter}.
        '''.format(
            player='' if not event.counter_id.player else event.counter_id.player + ' gets ',
            number='+' + str(event.value) if event.value >= 0 else str(event.value),
            counter=CounterName(event.counter_id.name).name,
        )
        s = s.strip()
        return s

    def _shuffle_event_to_str(self, event):
        s = '''
        {player} shuffles their {loc}.
        '''.format(
            player=event.location.player,
            loc=LocationName(event.location.name).name,
        )
        s = s.strip()
        return s

    def log(self, event):
        self._log.append(event)
        event_str = ''
        if type(event) == CardMoveEvent:
            event_str = self._card_move_event_to_str(event)
        elif type(event) == CounterEvent:
            event_str = self._counter_event_to_str(event)
        elif type(event) == ShuffleEvent:
            event_str = self._shuffle_event_to_str(event)
        print(event_str)


