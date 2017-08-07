import unittest

from core.card_distribution import CardDistribution
from core.game_state import GameState


class GameStateTest(unittest.TestCase):
    def test_create_default_game_state(self):
        supply = CardDistribution()
        supply.add(card=1, amount=1)
        supply.add(card=2, amount=2)
        starting_cards = ([3] * 3) + ([4] * 4)
        names = ['p1', 'p2']
        game_state = GameState(player_names=names, supply=supply, starting_cards=starting_cards)
        for name in names:
            player_state = game_state.get_player_state(name)
            self.assertEqual(
                player_state.draw_pile.distribution, CardDistribution(starting_cards),
                'Each player has the starting cards in their draw pile.'
            )


if __name__ == '__main__':
    unittest.main()
