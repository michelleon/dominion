from collections import Counter
from copy import deepcopy


class CardDistribution:
    """
    Represents cards to counts mapping
    """
    def __init__(self, initial_card_list=None):
        initial_card_list = initial_card_list or []
        self._card_counter = Counter(initial_card_list)

    def __iter__(self):
        for card, count in self.cards_to_counts().items():
            for i in range(count):
                yield card

    def __repr__(self):
        s = 'CardDistribution\n'
        card_strs = ['%s:\t%d' % (str(key), val) for key, val in self._card_counter.items()]
        s += '\n'.join(card_strs)
        s += '\n'
        return s

    def count(self, card):
        return self._card_counter[card]

    def cards_to_counts(self):
        return dict(self._card_counter)

    def empty(self):
        self._card_counter = Counter()

    def add(self, card, amount = 1):
        self._card_counter[card] += amount

    def size(self):
        return sum(self._card_counter.values())

    def subtract(self, card, amount = 1):
        self._card_counter.subtract({ card: amount })

    def deepcopy(self):
        distribution = CardDistribution()
        distribution._card_counter = deepcopy(self._card_counter)
        return distribution 

    def __eq__(self, other):
        return self._card_counter == other._card_counter

        