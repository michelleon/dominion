from core.card_distribution import CardDistribution
from core.card_stack import CardStack


class PlayerState(object):
    def __init__(self, name, starting_cards):
        self._name = name
        self.draw_pile = CardStack(starting_cards)
        self.discard = CardStack()
        self.in_play = CardDistribution()
        self.hand = CardDistribution()
        self.actions_left = 1
        self.buys_left = 1

    def deepcopy(self):
        new_state = PlayerState(self._name, [])
        new_state.draw_pile = self.draw_pile.deepcopy()
        new_state.discard = self.discard.deepcopy()
        new_state.in_play = self.in_play.deepcopy()
        new_state.hand = self.hand.deepcopy()
        new_state.actions_left = self.actions_left
        new_state.buys_left = self.buys_left
        return new_state
