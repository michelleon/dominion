from collections import Counter
import random
import unittest

from base_set.cards import KINGDOM_CARDS
from core.agents.test import TestAgent
from core.game_controller import GameController


class TestLogger:
    def __init__(self):
        self._log = []

    def log(self, event, audience=None):
        self._log.append((event, audience))

    def get_log(self):
        return self._log


class GameControllerTest(unittest.TestCase):
    def create_controller(self):
        gc = GameController(
            players=[TestAgent('p1'), TestAgent('p2')],
            card_set=KINGDOM_CARDS,
            log=TestLogger(),
        )
        return gc

    def test_create_game_controller(self):
        controller = self.create_controller()

    def test_run_game(self):
        random.seed(1221)
        controller = self.create_controller()
        winner = controller.run()

    def test_get_winner_indices(self):
        controller = self.create_controller()
        winners = controller.get_winner_indices(
            start_turn_index=0, next_turn_index=0, scores=[10, 10]
        )
        self.assertEqual(
            set(winners), set([0, 1]),
            'If score is tied and both players had the same number of turns then they tie.'
        )

        winners = controller.get_winner_indices(
            start_turn_index=0, next_turn_index=1, scores=[10, 10]
        )
        self.assertEqual(
            winners, [1],
            'If score is tied and one player had fewer turns then they win.'
        )

        winners = controller.get_winner_indices(
            start_turn_index=1, next_turn_index=0, scores=[10, 10]
        )
        self.assertEqual(
            winners, [0],
            'If score is tied and one player had fewer turns then they win.'
        )

        winners = controller.get_winner_indices(
            start_turn_index=0, next_turn_index=1, scores=[11, 10]
        )
        self.assertEqual(
            winners, [0],
            'If one player had more turns but also has more points then they win.'
        )


if __name__ == '__main__':
    unittest.main()
