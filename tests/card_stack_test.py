import unittest
from core.card_stack import CardStack
from core.card_stack import UnorderedCardStack
from core.card_stack import StackPosition


class CardStackTest(unittest.TestCase):
    def setUp(self):
        self.card_stack = CardStack(['a'])

    def test_has_card(self):
        self.assertTrue(self.card_stack.has_card('a'))
        self.assertFalse(self.card_stack.has_card('b'))

    def test_add(self):
        card_stack = CardStack([])
        card_stack.add('b')
        self.assertTrue(card_stack.has_card('b'))
        self.assertEqual(card_stack.distribution.count('b'), 1)
        cards = card_stack.draw(1)
        self.assertEqual(cards, ['b'])
        card_stack.add(['a', 'b', 'c'])
        cards = card_stack.draw(1)
        self.assertEqual(cards, ['a'])
        card_stack.add('a', StackPosition.BOTTOM)
        cards = card_stack.draw(1)
        self.assertEqual(cards, ['b'])
        cards = card_stack.draw(2)
        self.assertEqual(cards, ['c', 'a'])

    def test_add_to_bottom(self):
        card_stack = CardStack()
        card_stack.add(['a', 'b', 'c'])
        card_stack.add(['d', 'e', 'f'], position=StackPosition.BOTTOM)
        cards = card_stack.draw(5)
        self.assertEqual(cards, ['a', 'b', 'c', 'd', 'e'])

    def test_extract(self):
        card_stack = CardStack(['a', 'b', 'c', 'd', 'b', 'e'])
        extracted = card_stack.extract(['b'])
        self.assertEqual(extracted, ['b'])
        self.assertEqual(card_stack.size(), 5)
        self.assertEqual(card_stack.distribution.count('b'), 1)
        cards = card_stack.draw(card_stack.size())
        self.assertEqual(cards, ['a', 'c', 'd', 'b', 'e'])
        card_stack.add(cards)
        extracted = card_stack.extract(['b'])
        self.assertEqual(card_stack.distribution.count('b'), 0)

    def test_size(self):
        self.assertEqual(self.card_stack.size(), 1)
        self.card_stack.add('b')
        self.assertEqual(self.card_stack.size(), 2)

    def test_draw(self):
        self.card_stack.add('a')
        self.card_stack.add('b')
        self.card_stack.add('c')
        self.assertEqual(self.card_stack.draw(2), ['c', 'b'])
        self.assertEqual(self.card_stack.size(), 2)
        self.assertEqual(self.card_stack.distribution.size(), 2)

    def test_shuffle(self):
        self.card_stack.add('b')
        self.card_stack.add('c')
        self.card_stack.shuffle()

        self.assertEqual(self.card_stack.size(), 3)
        self.assertTrue(self.card_stack.has_card('a'))
        self.assertTrue(self.card_stack.has_card('b'))
        self.assertTrue(self.card_stack.has_card('c'))

        stack = CardStack(['a', 'b', 'c'])
        unshuffled_stack = stack.deepcopy()
        found_difference = False
        for _ in range(10):
            stack.shuffle()
            if stack._stack != unshuffled_stack._stack:
                found_difference = True
                break

        self.assertTrue(found_difference)


    def test_deep_copy(self):
        self.card_stack.add('b')
        stack_copy = self.card_stack.deepcopy()
        self.assertEqual(self.card_stack.size(), stack_copy.size())
        self.assertEqual(self.card_stack._stack, stack_copy._stack)
        self.assertEqual(self.card_stack.distribution, stack_copy.distribution)

    def test_empty(self):
        self.card_stack.empty()
        self.assertEqual(self.card_stack.size(), 0, 'Stack size should be 0 after empty.')
        self.assertEqual(
            {}, self.card_stack.distribution.cards_to_counts(),
            'Distribution should be empty after emptying.'
        )

    def test_peek(self):
        stack = CardStack(['a', 'b', 'c'])
        self.assertEqual(stack.peek(0), 'a')
        self.assertEqual(stack.peek(1), 'b')
        self.assertEqual(stack.size(), 3)
        stack.draw(1)
        self.assertEqual(stack.peek(0), 'b')
        self.assertEqual(stack.peek(1), 'c')


class UnorderedCardStackTest(unittest.TestCase):
    def test_add(self):
        stack = UnorderedCardStack()
        stack.add('a')
        stack.add('b')
        self.assertEqual(stack.size(), 2)
        self.assertEqual(set(stack), {'a', 'b'})

    def test_empty(self):
        stack = UnorderedCardStack(['a', 'b', 'b', 'c'])
        self.assertEqual(stack.size(), 4)
        stack.empty()
        self.assertEqual(stack.size(), 0)
        self.assertEqual(stack.distribution.size(), 0)

    def test_extract(self):
        stack = UnorderedCardStack(['a', 'b', 'b', 'c'])
        cards = stack.extract(['b'])
        self.assertEqual(cards, ['b'])
        self.assertEqual(stack.size(), 3)
        self.assertTrue(stack.has_card('b'))

    def test_has_card(self):
        stack = UnorderedCardStack(['a', 'b', 'b', 'c'])
        for card in ('a', 'b', 'c'):
            self.assertTrue(stack.has_card(card))
        self.assertFalse(stack.has_card('card that does not exist'))
        self.assertFalse(stack.has_card('d'))
        stack.add('d')
        self.assertTrue(stack.has_card('d'))

    def test_shuffle(self):
        stack = UnorderedCardStack(['a', 'b', 'c', 'd'])
        org = list(stack)
        stack.shuffle()
        after = list(stack)
        self.assertEqual(sorted(org), sorted(after))

    def test_size(self):
        stack = UnorderedCardStack()
        self.assertEqual(stack.size(), 0)
        stack.add(['a', 'b'])
        self.assertEqual(stack.size(), 2)


if __name__ == '__main__':
    unittest.main()