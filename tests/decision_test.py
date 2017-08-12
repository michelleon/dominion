import unittest

from core.decision import Decision


class DecisionTest(unittest.TestCase):
    def test_is_valid(self):
        single_choice_decision = Decision(options=[0, 1, 2], min=1, max=1)
        self.assertTrue(
            single_choice_decision.is_valid(1),
            'Choosing a single option from the list is valid.'
        )
        self.assertFalse(
            single_choice_decision.is_valid(3),
            'Choosing a single option not from the list is not valid.'
        )
        self.assertTrue(
            single_choice_decision.is_valid([1]),
            'Choosing a single option presented as a list is valid.'
        )
        self.assertFalse(
            single_choice_decision.is_valid([1, 2]),
            'Choosing multiple options from the list is not valid.'
        )
        self.assertFalse(
            single_choice_decision.is_valid([]),
            'Choosing no options from the list is not valid.'
        )

        multi_choice_decision = Decision(options=[0, 1, 2], min=2, max=3)
        self.assertTrue(
            multi_choice_decision.is_valid([1, 2]),
            'Choosing multiple options from the list is valid as long as the number chosen '
            'is between min and max inclusive.'
        )
        self.assertFalse(
            multi_choice_decision.is_valid([1]),
            'Choosing fewer options from the list than the min is not valid.'
        )

    def test_choose_random(self):
        single_choice_decision = Decision(options=[0, 1, 2], min=1, max=1)
        choices = set([tuple(single_choice_decision.choose_random()) for i in range(100)])
        self.assertTrue(len(choices) > 1, 'Random choice should not always be the same')
        lengths = set(map(lambda x: len(x), choices))
        self.assertTrue(
            list(lengths) == [1], 'All choices should be length one when min and max are one'
        )

        min_, max_ = (2, 3)
        multi_choice_decision = Decision(options=[0, 1, 2], min=min_, max=max_)
        choices = set([tuple(multi_choice_decision.choose_random()) for i in range(100)])
        self.assertTrue(len(choices) > 1, 'Random choice should not always be the same')
        lengths = set(map(lambda x: len(x), choices))
        possible_lengths = set(range(min_, max_ + 1))
        self.assertEqual(
            lengths, possible_lengths, 'All choices should be length one when min and max are one'
        )

    def test_there_is_no_choice(self):
        single_choice_decision = Decision(options=[0, 1, 2], min=1, max=1)
        self.assertFalse(
            single_choice_decision.there_is_no_choice(),
            'A single choice with multiple options contains a choice.'
        )
        binary_decision = Decision(options=[0], min=0, max=1)
        self.assertFalse(
            binary_decision.there_is_no_choice(),
            'If there is only one option but not choosing anything is allowed then there '
            'is still a choice.'
        )
        no_choice_decision = Decision(options=[0], min=1, max=1)
        self.assertTrue(
            no_choice_decision.there_is_no_choice(),
            'A single choice with only one option does not contain a choice.'
        )

        multi_no_choice_decision = Decision(options=[0, 1], min=2, max=2)
        self.assertTrue(
            multi_no_choice_decision.there_is_no_choice(),
            'If the number of options matches the number of required chocies then there is no choice.'
        )
        multi_no_choice_decision2 = Decision(options=[0, 1], min=2, max=3)
        self.assertTrue(
            multi_no_choice_decision2.there_is_no_choice(),
            'If the number of options matches the minimum number of choices, even if the max is '
            'greater, there still is no choice.'
        )
        multi_choice_decision = Decision(options=[0, 1, 2], min=2, max=3)
        self.assertFalse(
            multi_choice_decision.there_is_no_choice(),
            'If the min and max are not equal and there are more options than the min '
            'then there is a choice'
        )


if __name__ == '__main__':
    unittest.main()
