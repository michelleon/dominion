import unittest

from base_set.cards import CopperCard
from base_set.cards.vassal import VassalCard
from base_set.cards.vassal import VassalDecision
from core.agents.base import BaseAgent
from core.card_stack import UnorderedCardStack
from core.game_state import GameState
from core.locations import Location
from core.locations import LocationName


class NullLogger:
    def log(self, event):
        pass


class NeverVassalAgent(BaseAgent):
    def make_decision(self, decision, known_state=None):
        if isinstance(decision, VassalDecision):
            return []
        return decision.choose_random()


class AlwaysVassalAgent(BaseAgent):
    def make_decision(self, decision, known_state=None):
        if isinstance(decision, VassalDecision):
            return decision.options
        return decision.choose_random()


class VassalCardTest(unittest.TestCase):
    def create_game_state(self, starting_deck):
        supply = UnorderedCardStack([VassalCard])
        starting_deck = starting_deck
        names = ['p1', 'p2']
        logger = NullLogger()
        game_state = GameState(
            player_names=names, supply=supply, starting_deck=starting_deck, logger=logger
        )
        return game_state

    def test_top_card_not_action(self):
        game_state = self.create_game_state([CopperCard, CopperCard])
        player = game_state.get_current_player_name()
        VassalCard.play(game_state)
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        self.assertEqual(discard.peek(), CopperCard)
    
    def test_no_cards_in_deck_some_in_discard(self):
        game_state = self.create_game_state([])
        player = game_state.get_current_player_name()
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        discard.add([CopperCard, CopperCard])
        VassalCard.play(game_state)
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        self.assertEqual(discard.peek(), CopperCard)
        draw_pile = game_state.get_location(Location(player, LocationName.DRAW_PILE))
        self.assertEqual(draw_pile.peek(), CopperCard)

    def test_no_cards_in_deck_or_discard(self):
        game_state = self.create_game_state([])
        player = game_state.get_current_player_name()
        VassalCard.play(game_state)
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        draw_pile = game_state.get_location(Location(player, LocationName.DRAW_PILE))
        self.assertEqual(draw_pile.size(), 0)
        self.assertEqual(discard.size(), 0)

    def test_top_card_is_action_choose_not_to_play_it(self):
        game_state = self.create_game_state([VassalCard, CopperCard])
        game_state.set_agents([NeverVassalAgent('p1'), NeverVassalAgent('p2')])
        player = game_state.get_current_player_name()
        VassalCard.play(game_state)
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        draw_pile = game_state.get_location(Location(player, LocationName.DRAW_PILE))
        self.assertEqual(discard.peek(), VassalCard)
        self.assertEqual(draw_pile.peek(), CopperCard)

    def test_top_cards_are_actions_choose_to_play_them(self):
        game_state = self.create_game_state([VassalCard, VassalCard, CopperCard, CopperCard])
        game_state.set_agents([AlwaysVassalAgent('p1'), AlwaysVassalAgent('p2')])
        player = game_state.get_current_player_name()
        VassalCard.play(game_state)
        discard = game_state.get_location(Location(player, LocationName.DISCARD))
        in_play = game_state.get_location(Location(player, LocationName.IN_PLAY))
        draw_pile = game_state.get_location(Location(player, LocationName.DRAW_PILE))
        self.assertEqual(in_play.size(), 2)  # Doesn't include the artificially played one
        self.assertEqual(discard.size(), 1)
        self.assertEqual(draw_pile.size(), 1)
        self.assertEqual(discard.peek(), CopperCard)
        self.assertEqual(draw_pile.peek(), CopperCard)
