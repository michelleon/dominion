import random
import unittest

from core.card_distribution import CardDistribution
from core.card_stack import StackPosition
from core.card_stack import UnorderedCardStack
from core.events import CardEventType
from core.events import CardMoveEvent
from core.events import ShuffleEvent
from core.game_state import GameState
from core.locations import Location
from core.locations import LocationName


class TestLogger:
    def __init__(self):
        self._log = []

    def log(self, event):
        self._log.append(event)

    def get_log(self):
        return self._log


class GameStateTest(unittest.TestCase):
    def create_default_game_state(self):
        supply = UnorderedCardStack()
        supply.add(cards=[1])
        supply.add(cards=[2, 2])
        names = ['p1', 'p2']
        logger = TestLogger()
        game_state = GameState(
            player_names=names, supply=supply, starting_deck=[], logger=logger
        )
        return game_state

    def test_create_game_state(self):
        supply = UnorderedCardStack()
        supply.add(cards=[1])
        supply.add(cards=[2, 2])
        names = ['p1', 'p2']
        logger = TestLogger()
        game_state = GameState(
            player_names=names, supply=supply, starting_deck=[], logger=logger
        )
        # Check trash exists
        trash = game_state.get_location(Location(None, LocationName.TRASH))
        self.assertEqual(type(trash), UnorderedCardStack)
        # Check player hands exist
        for name in names:
            hand = game_state.get_location(Location(name, LocationName.HAND))
            self.assertEqual(type(trash), UnorderedCardStack)

    def test_shuffle(self):
        game_state = self.create_default_game_state()
        current_player = game_state.get_current_player_name()
        draw_pile_location = Location(current_player, LocationName.DRAW_PILE)
        draw_pile = game_state.get_location(draw_pile_location)
        for i in range(100):
            draw_pile.add(i)
        self.assertEqual(
            list(draw_pile), list(range(100)[::-1]),
            'Draw pile is in the order cards were added.'
        )
        game_state.shuffle(Location(current_player, LocationName.DRAW_PILE))
        self.assertNotEqual(
            list(draw_pile), list(range(100)[::-1]),
            'Order of draw pile has changed after shuffling.'
        )
        event = ShuffleEvent(draw_pile_location)
        self.assertEqual(
            game_state.logger.get_log(), [event],
            'Only shuffle event was logged.'
        )

    def test_draw_when_enough_cards_in_draw_pile(self):
        game_state = self.create_default_game_state()
        current_player = game_state.get_current_player_name()
        draw_pile_location = Location(current_player, LocationName.DRAW_PILE)
        draw_pile = game_state.get_location(draw_pile_location)
        for i in range(10):
            draw_pile.add(i)
        game_state.draw(5)
        self.assertEqual(draw_pile.size(), 5)
        hand_location = Location(current_player, LocationName.HAND)
        hand = game_state.get_location(hand_location)
        self.assertEqual(hand.size(), 5)
        event = (
            CardMoveEvent(
                [9, 8, 7, 6, 5], draw_pile_location, StackPosition.TOP,
                hand_location, None, CardEventType.DRAW
            )
        )
        self.assertEqual(
            game_state.logger.get_log(), [event]
        )

    def test_draw_when_enough_cards_in_discard_pile(self):
        self.maxDiff = None
        random.seed(0)
        game_state = self.create_default_game_state()
        current_player = game_state.get_current_player_name()
        draw_pile_location = Location(current_player, LocationName.DRAW_PILE)
        draw_pile = game_state.get_location(draw_pile_location)
        for i in range(3):
            draw_pile.add(i)
        discard_location = Location(current_player, LocationName.DISCARD)
        discard = game_state.get_location(discard_location)
        for i in range(3, 6):
            discard.add(i)
        game_state.draw(5)
        self.assertEqual(draw_pile.size(), 1)
        hand_location = Location(current_player, LocationName.HAND)
        hand = game_state.get_location(hand_location)
        self.assertEqual(hand.size(), 5)
        shuffle_event = ShuffleEvent(Location(current_player, LocationName.DISCARD))
        move_discard_under_deck_event = CardMoveEvent(
            cards=[5, 3, 4],  # Note this ordering depends on random seed being set
            from_location=Location(current_player, LocationName.DISCARD),
            from_position=StackPosition.TOP,
            to_location=Location(current_player, LocationName.DRAW_PILE),
            to_position=StackPosition.BOTTOM,
            type=CardEventType.MOVE
        )
        draw_event = CardMoveEvent(
            # Note that the ordering depends on the random seed being set
            [2, 1, 0, 5, 3], draw_pile_location, StackPosition.TOP,
            hand_location, None, CardEventType.DRAW
        )
        self.assertEqual(
            game_state.logger.get_log(), [
                shuffle_event,
                move_discard_under_deck_event,
                draw_event,
            ]
        )

    def test_play(self):
        game_state = self.create_default_game_state()
        current_player = game_state.get_current_player_name()
        hand_location = Location(current_player, LocationName.HAND)
        hand = game_state.get_location(hand_location)
        hand.add(1)
        game_state.play(1)
        in_play = game_state.get_location(Location(current_player, LocationName.IN_PLAY))
        self.assertEqual(in_play.size(), 1)
        self.assertEqual(hand.size(), 0)
        game_state.discard_location(Location(current_player, LocationName.IN_PLAY))
        self.assertEqual(in_play.size(), 0)


if __name__ == '__main__':
    unittest.main()
