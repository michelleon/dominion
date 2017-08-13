from collections import deque
from random import shuffle
from copy import deepcopy

from core.card_distribution import CardDistribution

class CardStack:
    """
    An ordered stack of cards.
    """
    def __init__(self, initial_card_list=None):
        initial_card_list = initial_card_list or []
        self.distribution = CardDistribution(initial_card_list)
        self._stack = deque(initial_card_list)

    # Use case: gain a card
    def add(self, card):
        self.distribution.add(card)
        self._stack.appendleft(card)

    # Use case: when removing from hand or picking from discard
    def extract(self, card):
        self.distribution.subtract(card)
        self._stack.remove(card)
        return card

    def has_card(self, card):
        return self.distribution.count(card) > 0

    def draw(self, amount):
        return [self._stack.popleft() for i in range(amount)]

    def add_to_bottom(self, card):
        self.distribution.add(card)
        self._stack.appendRight(card)

    def put_other_stack_underneath(self, stack):
        """
        Adds another stack underneath this one. The other stack will be empty after this
        operation.
        """
        cards = stack.to_list()
        self._stack.extend(cards)
        self.distribution.add_list(cards)
        stack.empty()

    def to_list(self):
        """
        Return all cards as a list.
        """
        return list(self._stack)

    def empty(self):
        self._stack = deque()
        self.distribution  = CardDistribution()

    def shuffle(self):
        shuffle(self._stack)

    def size(self):
        return len(self._stack)

    def deepcopy(self):
        card_stack = CardStack()
        card_stack.distribution = self.distribution.deepcopy()
        card_stack._stack = deepcopy(self._stack)
        return card_stack



        