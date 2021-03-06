import unittest

from core.card_distribution import CardDistribution


class CardDistributionTest(unittest.TestCase):
    def setUp(self):
        self.card_distribution = CardDistribution()

    def test_count(self):
        self.assertEqual(self.card_distribution.count('a'), 0)
        self.assertEqual(self.card_distribution.count('b'), 0)

    def test_add(self):
        self.card_distribution.add('a')
        self.assertEqual(self.card_distribution.count('a'), 1)
        self.card_distribution.add('a', 2)
        self.assertEqual(self.card_distribution.count('a'), 3)

    def test_subtract(self):
        self.card_distribution.add('a')
        self.assertEqual(self.card_distribution.count('a'), 1)
        self.card_distribution.subtract('a')
        self.card_distribution.subtract('a', 2)
        self.assertEqual(self.card_distribution.count('a'), -2)

    def test_comparator(self):
        other = CardDistribution(['a', 'a', 'b'])
        self.card_distribution.add('a')
        self.card_distribution.add('a')
        self.card_distribution.add('b')
        self.assertTrue(other == self.card_distribution)

    def test_size(self):
        dist = CardDistribution([1, 1, 2])
        self.assertEqual(dist.size(), 3)
        dist.subtract(1)
        self.assertEqual(dist.size(), 2)
        
    def test_iter(self):
        dist = CardDistribution([1, 1, 2])
        self.assertEqual(sorted(list(dist)), [1, 1, 2])
        dist.subtract(2)
        self.assertEqual(sorted(list(dist)), [1, 1])

    def test_empty(self):
        dist = CardDistribution([1, 1, 2])
        dist.empty()
        self.assertEqual(dist.size(), 0)


if __name__ == '__main__':
    unittest.main()