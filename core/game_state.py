from core.card_stack import CardStack
from core.card_stack import StackPosition
from core.card_stack import UnorderedCardStack
from core.counters import CounterId
from core.counters import CounterName
from core.counters import GLOBAL_COUNTERS
from core.events import CardEventType
from core.events import CardMoveEvent
from core.events import CounterEvent
from core.events import CounterEventType
from core.events import ShuffleEvent
from core.locations import GLOBAL_LOCATIONS
from core.locations import Location
from core.locations import LocationName


STACK_CLASS_BY_LOCATION_NAME = {
    LocationName.DRAW_PILE: CardStack,
    LocationName.HAND: UnorderedCardStack,
    LocationName.DISCARD: CardStack,
    LocationName.IN_PLAY: UnorderedCardStack,
    LocationName.TRASH: UnorderedCardStack,
    LocationName.SUPPLY: UnorderedCardStack,
    LocationName.SET_ASIDE: UnorderedCardStack,
}
COUNTER_VALUES_AT_TURN_START = {
    CounterName.ACTIONS: 1,
    CounterName.BUYS: 1,
    CounterName.COINS: 0,
}


class ImpossibleMoveEvent(Exception):
    pass


class GameState:
    """
    Represents all game state.
    """
    def __init__(self, player_names, supply, starting_deck, logger):
        """
        Parameters:
            player_names (list of str): List of the names of players in the order of turns.
            supply (`UnorderedCardStack`): Starting supply for the game.
            starting_deck (`UnorderedCardStack`): Cards each player will start with.
            logger (`GameLogger`): All changes to game state will be logged here.
        """
        self.logger = logger
        self.player_names = player_names
        self._counters = self._create_counters(player_names)
        self._locations = self._create_locations(player_names)
        for player in player_names:
            stack = self.get_location(Location(player, LocationName.DRAW_PILE))
            stack.add(list(starting_deck))
        self._locations[Location(None, LocationName.SUPPLY)] = supply
        self._current_player_index = 0

    def _create_locations(self, player_names):
        """
        Create a dict of `Location` -> CardStack for all locations
        in a starting game state given the list of player names.
        """
        locations = {}
        for loc_name, stack_class in STACK_CLASS_BY_LOCATION_NAME.items():
            stack_class = STACK_CLASS_BY_LOCATION_NAME[loc_name]
            if loc_name in GLOBAL_LOCATIONS:
                locations[Location(None, loc_name)] = stack_class()
            else:
                for player in player_names:
                    locations[Location(player, loc_name)] = stack_class()
        return locations

    def _create_counters(self, player_names):
        """
        Create a dict of `CounterId` -> int for all game state counters
        in a starting game state given the list of player names.
        """
        counters = {}
        for counter_name in GLOBAL_COUNTERS:
            counters[CounterId(None, counter_name)] = 0
        return counters

    def _shuffle_discard_into_draw(self, player):
        """
        Shuffle the discard pile of the player and put it under their draw pile.
        """
        discard_location = Location(player, LocationName.DISCARD)
        number = self.get_location(discard_location).size()
        discard_is_empty_so_no_action_required = (number == 0)
        if discard_is_empty_so_no_action_required:
            return
        self.shuffle(discard_location)
        self.move(
            cards=None,
            number=number,
            from_location=Location(player, LocationName.DISCARD),
            from_position=StackPosition.TOP,
            to_location=Location(player, LocationName.DRAW_PILE),
            to_position=StackPosition.BOTTOM,
            event_type=CardEventType.MOVE,
        )

    def get_current_player_name(self):
        """
        Return the name of the player whose turn it is. This is not necessarily the player
        who the game is waiting on to make a decision.
        """
        return self.player_names[self._current_player_index]

    def get_counter(self, counter_id):
        """
        Return the value of a counter.
        """
        return self._counters[counter_id]

    def get_deck(self, player):
        """
        Returns a list of Cards in the players deck. "Deck" refers to all cards belonging
        to the player including the ones in their hand, discard, in play, and set aside.
        """
        cards = []
        for loc_name in STACK_CLASS_BY_LOCATION_NAME:
            if loc_name in GLOBAL_LOCATIONS:
                continue
            cards += list(self.get_location(Location(player, loc_name)))
        return cards

    def get_location(self, location):
        return self._locations[location]

    def reset_counters_for_new_turn(self):
        """
        Updates all counters for the beginning of a new turn.
        """
        for counter_name, value in COUNTER_VALUES_AT_TURN_START.items():
            self.set_counter(CounterId(None, counter_name), value)

    def move(self, 
            cards, number, from_location, from_position, to_location, to_position, event_type):
        """
        Move one or more cards from one location to another.

        Logs a `CardMoveEvent` describing the move.

        Parameters:
            cards (nullable, list of `Card`): List of cards to be moved. This can be None if
                the number parameter is set.
            number (nullable, int): Number of cards to move. This should only be set if cards is
                None. In that case the instruction is to move the first number cards from the
                from_location to the to_location.
            from_location (`Location`): Location to move the cards from.
            from_position (`StackPosition`): Position of the cards in the from location.
            to_location (`Location`): Location to move the cards to.
            to_position (`StackPosition`): Position of the cards in the to location.
            event_type (`CardMoveEventType`): Type of the event. The reason the cards were moved.

        Raises:
            ImpossibleMoveEvent: If the move event is not possible in the current
                game state.
        """
        if bool(cards) == bool(number):
            raise ImpossibleMoveEvent('Either cards or number must be specified, but not both.')
        if number:
            from_stack = self.get_location(from_location)
            to_stack = self.get_location(to_location)
            cards = from_stack.draw(number, from_position)
            to_stack.add(cards, to_position)
            # To do handle privacy here, not all player should see what was moved.
            self.logger.log(
                CardMoveEvent(
                    cards, from_location, from_position, to_location, to_position, event_type
                )
            )
            return
        from_stack = self.get_location(from_location)
        cards = from_stack.extract(cards)
        to_stack = self.get_location(to_location)
        to_stack.add(cards, to_position)
        self.logger.log(
            CardMoveEvent(
                cards, from_location, from_position, to_location, to_position, event_type
            )
        )
        return

    def update_counter(self, counter_id, delta):
        self._counters[counter_id] += delta
        event = CounterEvent(counter_id, CounterEventType.UPDATE, delta)
        self.logger.log(event)

    def set_counter(self, counter_id, value):
        self._counters[counter_id] = value
        event = CounterEvent(counter_id, CounterEventType.SET, value)
        
    def reveal(self, location, cards, position, number):
        """
        Reveal a card or cards to all players.

        Parameters:
            ToDo
        """
        pass

    def shuffle(self, location):
        """
        Shuffle the cards at the location.
        """
        stack = self.get_location(location)
        stack.shuffle()
        event = ShuffleEvent(location)
        self.logger.log(event)

    def draw(self, number, player=None):
        """
        Draws `number` cards to the given player's hand.
        """
        player = player or self.get_current_player_name()
        draw_stack = self.get_location(Location(player, LocationName.DRAW_PILE))
        if draw_stack.size() < number:
            self._shuffle_discard_into_draw(player)
        number_to_draw = min(number, draw_stack.size())
        if number_to_draw == 0:
            return
        self.move(
            cards=None,
            number=number_to_draw,
            from_location=Location(player, LocationName.DRAW_PILE),
            from_position=StackPosition.TOP,
            to_location=Location(player, LocationName.HAND),
            to_position=None,
            event_type=CardEventType.DRAW            
        )

    def look_at(self, look_event):
        """
        Reveal a card or cards to a specific player
        """
        pass

    def play(self, card, player=None, from_location=None):
        """
        Causes the player to play the card. This just moves the card to play
        from the player's hand it does not trigger the cards logic to be executed.
        """
        player = player or self.get_current_player_name()
        from_location = from_location or Location(player, LocationName.HAND)
        self.move(
            cards=[card],
            number=None,
            from_location=from_location,
            from_position=None,
            to_location=Location(player, LocationName.IN_PLAY),
            to_position=None,
            event_type=CardEventType.PLAY  
        )

    def discard(self, cards, player=None, location=None):
        """
        Causes the player to discard the cards. The first card in the list will be the one
        on top of the discard pile after discarding them.
        """
        player = player or self.get_current_player_name()
        location = location or Location(player, LocationName.HAND)
        self.move(
            cards=cards,
            number=None,
            from_location=location,
            from_position=None,
            to_location=Location(player, LocationName.DISCARD),
            to_position=None,
            event_type=CardEventType.DISCARD  
        )

    def discard_location(self, location):
        """
        Move all cards in location to the discard.
        """
        cards = list(self.get_location(location))
        if not cards:
            return
        self.discard(cards, player=location.player, location=location)

    def buy(self, card):
        """
        Causes the current player to buy the card.
        """
        player = self.get_current_player_name()
        self.move(
            cards=[card],
            number=None,
            from_location=Location(None, LocationName.SUPPLY),
            from_position=None,
            to_location=Location(player, LocationName.DISCARD),
            to_position=None,
            event_type=CardEventType.BUY  
        )

    def gain(self, card, player=None):
        """
        Causes the player to gain the card.
        """
        player = player or self.get_current_player_name()
        self.move(
            cards=[card],
            number=None,
            from_location=Location(None, LocationName.SUPPLY),
            from_position=None,
            to_location=Location(player, LocationName.DISCARD),
            to_position=None,
            event_type=CardEventType.GAIN  
        )

    def trash(self, card, player=None):
        """
        Causes the player to trash the card.
        """
        player = player or self.get_current_player_name()
        self.move(
            cards=[card],
            number=None,
            from_location=Location(player, LocationName.HAND),
            from_position=None,
            to_location=Location(None, LocationName.TRASH),
            to_position=None,
            event_type=CardEventType.TRASH  
        )
