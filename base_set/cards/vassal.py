from core.card import CardType
from core.card import KingdomCard
from core.card_stack import StackPosition
from core.counters import CounterId
from core.counters import CounterName
from core.decision import Decision
from core.events import CardEventType
from core.locations import Location
from core.locations import LocationName


class VassalDecision(Decision):
    def __init__(self, card):
        self.options = [card]
        self.min = 0
        self.max = 1


class VassalCard(KingdomCard):
    """
    +2 coins

    Discard the top card of your deck. If it's an Action card, you may play it.
    """
    types = (CardType.ACTION,)
    base_cost = 3

    @classmethod
    def play(cls, game_state):
        player = game_state.get_current_player_name()
        game_state.update_counter(counter_id=CounterId(None, CounterName.COINS), delta=2)
        game_state.shuffle_discard_in_if_insufficient_cards(1)
        draw_stack = game_state.get_location(Location(player, LocationName.DRAW_PILE))
        if draw_stack.size() < 1:
            return
        game_state.move(
            cards=None,
            number=1,
            from_location=Location(player, LocationName.DRAW_PILE),
            from_position=StackPosition.TOP,
            to_location=Location(player, LocationName.DISCARD),
            to_position=StackPosition.TOP,
            event_type=CardEventType.DISCARD            
        )
        discard_stack = game_state.get_location(Location(player, LocationName.DISCARD))
        top_card = discard_stack.peek()
        if CardType.ACTION not in top_card.types:
            return
        decision = VassalDecision(top_card)
        agent = game_state.get_agent(player)
        choice = agent.make_decision(decision)
        assert decision.is_valid(choice)
        if not choice:
            return
        game_state.move(
            cards=choice,
            number=None,
            from_location=Location(player, LocationName.DISCARD),
            from_position=StackPosition.TOP,
            to_location=Location(player, LocationName.IN_PLAY),
            to_position=None,
            event_type=CardEventType.PLAY            
        )     
        card = choice[0]
        card.play(game_state)
