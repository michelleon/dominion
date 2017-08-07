import unittest

from base_set.instructions.draw_cards_instruction import DrawCardsInstruction
from core.card_distribution import CardDistribution
from core.game_state import GameState


class TestLogger(object):
    def __init__(self):
        self._log = []

    def info(self, msg):
        self._log.append(msg)

    def has_logged_msg(self, msg):
        return msg in self._log


class DrawCardsInstructionTest(unittest.TestCase):
    def create_game_state(self):
        supply = CardDistribution()
        supply.add(card=1, amount=1)
        supply.add(card=2, amount=2)
        starting_cards = ([3] * 3) + ([4] * 4)
        names = ['p1', 'p2']
        return GameState(player_names=names, supply=supply, starting_cards=starting_cards)

    def test_cards_drawn_from_draw_pile_to_hand(self):
        game_state = self.create_game_state()
        player_state = game_state.get_player_state('p1')
        cards_in_draw_pile_before_draw = player_state.draw_pile.size()
        cards_in_hand_before_draw = player_state.hand.size()
        number_to_draw = 5
        instruction = DrawCardsInstruction(number_to_draw=number_to_draw, target_player='p1')
        logger = TestLogger()
        instruction.execute(game_state, logger=logger)
        cards_in_draw_pile_after_draw = player_state.draw_pile.size()
        cards_in_hand_after_draw = player_state.hand.size()
        self.assertEqual(
            cards_in_draw_pile_after_draw + number_to_draw, cards_in_draw_pile_before_draw,
            'Players draw pile is smaller by the number of drawn cards.'
        )
        self.assertEqual(
            cards_in_hand_after_draw - number_to_draw, cards_in_hand_before_draw,
            'Players hand pile is larger by the number of drawn cards.'
        )
        self.assertTrue(logger.has_logged_msg('p1 drew 5 cards.'))


if __name__ == '__main__':
    unittest.main()
