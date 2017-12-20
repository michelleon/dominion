from collections import Counter
import unittest

from base_set.cards import CopperCard
from base_set.cards import GoldCard
from base_set.cards import SilverCard
from base_set.cards.mine import MineCard
from base_set.cards.mine import MineGainDecision
from base_set.cards.mine import MineTrashDecision
from core.agents.base import BaseAgent
from core.card_stack import UnorderedCardStack
from core.game_state import GameState
from core.locations import Location
from core.locations import LocationName


class NullLogger:
    def log(self, event):
        pass


class MineUpgradeAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super(MineUpgradeAgent, self).__init__(*args, **kwargs)
        self._decision_counts = Counter()

    def get_decision_count(self, decision_class):
        return self._decision_counts[decision_class]

    def incr_decision_count(self, decision_class):
        self._decision_counts[decision_class] += 1

    def make_decision(self, decision, known_state=None):
        self.incr_decision_count(decision.__class__)
        if isinstance(decision, MineTrashDecision):
            if SilverCard in decision.options:
                return [SilverCard]
            elif CopperCard in decision.options:
                return [CopperCard]
            return []
        elif isinstance(decision, MineGainDecision):
            if GoldCard in decision.options:
                return [GoldCard]
            elif SilverCard in decision.options:
                return [SilverCard]
            else:
                return decision.choose_random()
        return decision.choose_random()


class MineCardTest(unittest.TestCase):
    def create_game_state(self, starting_deck):
        supply = UnorderedCardStack([MineCard, CopperCard, SilverCard, GoldCard])
        starting_deck = starting_deck
        names = ['p1', 'p2']
        logger = NullLogger()
        game_state = GameState(
            player_names=names, supply=supply, starting_deck=starting_deck, logger=logger
        )
        return game_state

    def test_no_treasure_in_hand(self):
        game_state = self.create_game_state([MineCard, MineCard])
        p1_agent = MineUpgradeAgent('p1')
        p2_agent = MineUpgradeAgent('p2')
        game_state.set_agents([p1_agent, p2_agent])
        player = game_state.get_current_player_name()
        MineCard.play(game_state)
        # Agent not given decision since they have no treasures in hand.
        self.assertEqual(p1_agent.get_decision_count(MineTrashDecision), 0)
        self.assertEqual(p1_agent.get_decision_count(MineGainDecision), 0)

    def test_upgrade_treasure(self):
        game_state = self.create_game_state([MineCard, CopperCard, CopperCard, SilverCard])
        p1_agent = MineUpgradeAgent('p1')
        p2_agent = MineUpgradeAgent('p2')
        game_state.set_agents([p1_agent, p2_agent])
        game_state.draw(4)
        player = game_state.get_current_player_name()
        MineCard.play(game_state)
        self.assertEqual(p1_agent.get_decision_count(MineTrashDecision), 1)
        self.assertEqual(p1_agent.get_decision_count(MineGainDecision), 1)
        hand = game_state.get_location(Location(player, LocationName.HAND))
        self.assertEqual(hand.size(), 4)
        self.assertTrue(GoldCard in list(hand))
        trash = game_state.get_location(Location(None, LocationName.TRASH))
        self.assertTrue(SilverCard in list(trash))
