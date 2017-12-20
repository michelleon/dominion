from core.card import CardType
from core.card import KingdomCard
from core.card import TreasureCard
from core.decision import Decision
from core.locations import Location
from core.locations import LocationName


class MineTrashDecision(Decision):
    def __init__(self, game_state):
        player = game_state.get_current_player_name()
        cards = set(game_state.get_location(Location(player, LocationName.HAND)))
        treasure_cards = [card for card in cards if issubclass(card, TreasureCard)]
        self.options = treasure_cards
        self.min = 0
        self.max = 1


class MineGainDecision(Decision):
    def __init__(self, game_state, max_cost):
        player = game_state.get_current_player_name()
        cards = set(game_state.get_location(Location(None, LocationName.SUPPLY)))
        treasure_cards_meeting_cost_constraint = [
            card for card in cards
            if issubclass(card, TreasureCard) and card.cost(game_state) <= max_cost
        ]
        self.options = treasure_cards_meeting_cost_constraint
        self.min = 1
        self.max = 1


class MineCard(KingdomCard):
    """
    You may trash a Treasure card from your hand. Gain a Treasure to your hand costing up
    to 3 more than it.
    """
    types = (CardType.ACTION,)
    base_cost = 5

    @classmethod
    def play(cls, game_state):
        decision = MineTrashDecision(game_state)
        if decision.there_is_no_choice():
            return
        player = game_state.get_current_player_name()
        agent = game_state.get_agent(player)
        choice = agent.make_decision(decision)
        assert decision.is_valid(choice)
        if not choice:
            return
        chosen_card = choice[0]
        max_cost = chosen_card.cost(game_state) + 3
        game_state.trash(chosen_card)
        decision = MineGainDecision(game_state, max_cost)
        choice = agent.make_decision(decision)
        assert decision.is_valid(choice)
        game_state.gain(choice[0], to_location=Location(player, LocationName.HAND))
