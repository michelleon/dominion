import unittest

from core.player_state import PlayerState


class PlayerStateTest(unittest.TestCase):
    def test_create_default_player_state(self):
        starting_cards = [1, 2, 3]
        player_state = PlayerState(name='test', starting_cards=starting_cards)
        self.assertTrue(
            player_state.draw_pile.size() == len(starting_cards),
            'PlayerState starts with all passed starting_cards in the draw pile.'
        )

    def test_deep_copy(self):
        starting_cards = [1, 2, 3]
        player_state = PlayerState(name='test', starting_cards=starting_cards)
        copied_state = player_state.deepcopy()
        card_stack_pairs = [
            (player_state.draw_pile, copied_state.draw_pile),
            (player_state.discard, copied_state.discard),
        ]
        card_dist_pairs = [
            (player_state.in_play, copied_state.in_play),
            (player_state.hand, copied_state.hand),
        ]
        for original, copied in card_stack_pairs:
            original.add(10)
            self.assertTrue(
                original.size() > copied.size(),
                'Adding to a stack in the original player state does not affect the copied state.'
            )
        for original, copied in card_dist_pairs:
            original.add(10)
            self.assertTrue(
                original.count(10) > copied.count(10),
                'Adding to a dist in the original player state does not affect the copied state.'
            )

if __name__ == '__main__':
    unittest.main()
