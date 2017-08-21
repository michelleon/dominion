from core.card import CardType
from core.card import KingdomCard
from core.decision import Decision
from core.locations import Location
from core.locations import LocationName


class ChapelDecision(Decision):
    def __init__(self, game_state):
        player = game_state.get_current_player_name()
        cards = list(game_state.get_location(Location(player, LocationName.HAND)))
        self.options = cards
        self.min = 0
        self.max = min(len(cards), 4)


class ChapelCard(KingdomCard):
    types = (CardType.ACTION,)
    base_cost = 2

    @classmethod
    def play(cls, game_state):
        decision = ChapelDecision(game_state)
        agent = game_state.get_agent(game_state.get_current_player_name())
        choice = agent.make_decision(decision)
        assert decision.is_valid(choice)
        for card in choice:
            game_state.trash(card)
