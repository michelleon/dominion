import random


class Decision:
    """
    Represents a decision that a player must make.
    """
    def __init__(self, options, min, max):
        """
        Parameters:
            options (list): List of possible choices.
            min (int): Minimum number of the choices that must be chosen.
            max (int): Maximum number of the choices that must be chosen.
        """
        self.options = options
        self.min = min
        self.max = max

    def choose_random(self):
        num_to_choose = random.randint(self.min, self.max)
        opt_copy = self.options[:]
        res = []
        for i in range(num_to_choose):
            pick = random.choice(opt_copy)
            opt_copy.remove(pick)
            res.append(pick)
        return res

    def there_is_no_choice(self):
        """
        Returns True if there is actually no choice to be made because there
        is only one valid options.
        """
        if self.min >= len(self.options):
            return True
        if not self.options:
            return True
        return False

    def is_valid(self, choices):
        """
        Checks if the choice is valid for this decision.
        """
        if type(choices) != list:
            choices = [choices]
        if len(choices) < self.min or len(choices) > self.max:
            return False
        opt_copy = self.options[:]
        for val in choices:
            if val not in opt_copy:
                return False
            opt_copy.remove(val)
        return True

class PlayTreasureDecision(Decision):
    pass

class PlayActionDecision(Decision):
    pass

class BuyDecision(Decision):
    pass
