import unittest
from core.card_stack import CardStack

class CardStackTest(unittest.TestCase):
    def setUp(self):
        self.card_stack = CardStack(['a'])

    def test_has_card(self):
        self.assertTrue(self.card_stack.has_card('a'))
        self.assertFalse(self.card_stack.has_card('b'))

    def test_add(self):
        self.card_stack.add('b')
        self.assertTrue(self.card_stack.has_card('b'))
        self.assertEqual(self.card_stack.distribution.count('b'), 1)

    def test_extract(self):
        self.card_stack.extract('a')
        self.assertFalse(self.card_stack.has_card('a'))
        self.assertEqual(self.card_stack.distribution.count('a'), 0)

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

    def test_to_list(self):
        stack = CardStack([1, 2, 3])
        self.assertEqual(stack.to_list(), [1, 2, 3])
        stack.add(4)
        self.assertEqual(stack.to_list(), [4, 1, 2, 3])

    def test_put_other_stack_underneath(self):
        stack = CardStack([1, 2, 3])
        other = CardStack([4, 5, 6])
        stack.put_other_stack_underneath(other)
        self.assertEqual(stack.size(), 6)
        self.assertEqual(other.size(), 0)
        self.assertEqual(stack.distribution.size(), 6)
        self.assertEqual(other.distribution.size(), 0)
        cards = stack.draw(6)
        self.assertEqual(
            cards,
            [1, 2, 3, 4, 5, 6]
        )


if __name__ == '__main__':
    unittest.main()