from collections import Counter
import unittest

from base_set.cards import CopperCard
from base_set.cards import GoldCard
from base_set.cards import SilverCard
from base_set.cards.poacher import PoacherCard
from core.agents.test import TestAgent
from core.card_stack import UnorderedCardStack
from core.counters import CounterId
from core.counters import CounterName
from core.game_state import GameState
from core.locations import Location
from core.locations import LocationName


class NullLogger:
    def log(self, event):
        pass


class PoacherCardTest(unittest.TestCase):
    def create_game_state(self, starting_deck, supply):
        starting_deck = starting_deck
        names = ['p1', 'p2']
        logger = NullLogger()
        game_state = GameState(
            player_names=names, supply=supply, starting_deck=starting_deck, logger=logger
        )
        return game_state

    def test_play_poacher_no_empty_supply_piles(self):
        starting_deck = [CopperCard] * 12
        game_state = self.create_game_state(
            starting_deck,
            supply=UnorderedCardStack([PoacherCard, CopperCard])
        )
        player = game_state.get_current_player_name()
        PoacherCard.play(game_state)
        hand = game_state.get_location(Location(player, LocationName.HAND))
        self.assertEqual(
            hand.size(), 1,
            'Poacher should have the player draw a card.'
        )
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        self.assertEqual(
            discard.size(), 0, 'If no empty supply piles no cards should be discarded.'
        )
        self.assertEqual(
            game_state.get_counter(CounterId(None, CounterName.COINS)),
            1,
            'Poacher should give the player one extra coin.'
        )
        self.assertEqual(
            game_state.get_counter(CounterId(None, CounterName.ACTIONS)),
            1,
            'Poacher should give the player one extra action.'
        )

    def test_play_poacher_with_empty_supply_piles(self):
        for num_empty_supply_piles in (1, 2, 3):
            cards_in_supply = [CopperCard, SilverCard, GoldCard]
            starting_deck = [CopperCard] * 20
            game_state = self.create_game_state(
                starting_deck,
                supply=UnorderedCardStack(cards_in_supply)
            )
            p1_agent = TestAgent('p1')
            p2_agent = TestAgent('p2')
            game_state.set_agents([p1_agent, p2_agent])
            supply = game_state.get_location(Location(None, LocationName.SUPPLY))
            # empty supply piles
            for i in range(num_empty_supply_piles):
                supply.extract([cards_in_supply[i]])
            player = game_state.get_current_player_name()
            start_hand_size = 5
            game_state.draw(start_hand_size)
            PoacherCard.play(game_state)
            hand = game_state.get_location(Location(player, LocationName.HAND))
            self.assertEqual(
                hand.size(), start_hand_size + 1 - num_empty_supply_piles,
                'Player should draw 1 card and then discard one for each empty supply pile.'
            )
            discard = game_state.get_location(Location(player, LocationName.DISCARD))
            self.assertEqual(
                discard.size(), num_empty_supply_piles,
                'Player should have discarded 1 card for each empty supply pile.'
            )
            self.assertEqual(
                game_state.get_counter(CounterId(None, CounterName.COINS)),
                1,
                'Poacher should give the player one extra coin.'
            )
            self.assertEqual(
                game_state.get_counter(CounterId(None, CounterName.ACTIONS)),
                1,
                'Poacher should give the player one extra action.'
            )


if __name__ == '__main__':
    unittest.main()
