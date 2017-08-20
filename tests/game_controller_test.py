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


if __name__ == '__main__':
    unittest.main()
