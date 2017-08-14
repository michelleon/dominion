from collections import deque
from copy import deepcopy
from random import shuffle
import enum

from core.card_distribution import CardDistribution


class StackPosition(enum.Enum):
    """
    References a position in a card stack.
    """
    TOP = 0
    BOTTOM = 1


class CardStack:
    """
    An ordered stack of cards.
    """
    def __init__(self, initial_card_list=None):
        initial_card_list = initial_card_list or []
        self.distribution = CardDistribution(initial_card_list)
        self._stack = deque(initial_card_list)

    def __iter__(self):
        for card in self._stack:
            yield card

    def add(self, cards, position=None):
        """
        Add a list of cards to the stack at the position. Position default to the top of stack.
        Note that `cards` can be a list or single item. If it's a single item it will be
        treated as if it were the only item in a list.

        If there are multiple cards in `cards` then they will be added such that the first card is
        higher in the stack than the last element.

        Parameters:
            cards (list): List of cards to add.
            position (optional, `StackPosition`): Position to add the cards to the stack.
        """
        position = position or StackPosition.TOP
        if type(cards) != list:
            cards = [cards]
        for card in cards:
            self.distribution.add(card)
        if position == StackPosition.TOP:
            # Have to reverse cards because extendleft reverses them
            self._stack.extendleft(cards[::-1])
        else:
            self._stack.extend(cards)

    def extract(self, cards):
        """
        Remove the cards from the stack and return them. If there are multiple of one of the cards
        in the stack then the one closest to the top will be extracted.
        """
        for card in cards:
            self.distribution.subtract(card)
            self._stack.remove(card)
        return cards

    def draw(self, amount, from_position=None):
        cards = []
        for i in range(amount):
            card = self._stack.popleft()
            cards.append(card)
            self.distribution.subtract(card)
        return cards

    def has_card(self, card):
        return self.distribution.count(card) > 0

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


class UnorderedCardStack(CardStack):
    """
    An unordered stack of cards. When an ordering is specified it will just be ignored.
    """
    def __init__(self, initial_card_list=None):
        initial_card_list = initial_card_list or []
        self.distribution = CardDistribution(initial_card_list)

    def __iter__(self):
        for card, count in self.distribution.cards_to_counts().items():
            for i in range(count):
                yield card

    def add(self, cards, position=None):
        if type(cards) != list:
            cards = [cards]
        for card in cards:
            self.distribution.add(card)

    def draw(self, amount, position=None):
        raise NotImplementedError('Can not draw from UnorderedCardStack')

    def empty(self):
        self.distribution.empty()

    def extract(self, cards):
        for card in cards:
            self.distribution.subtract(card)
        return cards

    def has_card(self, card):
        return self.distribution.count(card) > 0

    def shuffle(self):
        return        

    def size(self):
        return self.distribution.size()

    def deepcopy(self):
        card_stack = UnorderedCardStack()
        card_stack.distribution = self.distribution.deepcopy()
        return card_stack
