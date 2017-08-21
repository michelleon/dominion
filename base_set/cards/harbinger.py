from core.card import CardType
from core.card import KingdomCard
from core.card_stack import StackPosition
from core.counters import CounterId
from core.counters import CounterName
from core.decision import Decision
from core.events import CardEventType
from core.locations import Location
from core.locations import LocationName


class HarbingerDecision(Decision):
    def __init__(self, game_state):
        player = game_state.get_current_player_name()
        cards = list(game_state.get_location(Location(player, LocationName.DISCARD)))
        self.options = cards
        self.min = 0
        self.max = 1

class HarbingerCard(KingdomCard):
    types = (CardType.ACTION,)
    base_cost = 3

    @classmethod
    def play(cls, game_state):
        """
        +1 card
        +1 action
        Look through your discard pile. You may put that card on top of your deck
        """
        game_state.draw(1)
        game_state.update_counter(counter_id=CounterId(None, CounterName.ACTIONS), delta=1)

        decision = HarbingerDecision(game_state)
        agent = game_state.get_agent(game_state.get_current_player_name())
        chosen_cards = agent.make_decision(decision)
        assert decision.is_valid(chosen_cards)
        if chosen_cards:
            game_state.move(
                cards=chosen_cards,
                number=None,
                from_location=Location(agent.name(), LocationName.DISCARD),
                from_position=None,
                to_location=Location(agent.name(), LocationName.DRAW_PILE),
                to_position=StackPosition.TOP,
                event_type=CardEventType.MOVE            
            )


