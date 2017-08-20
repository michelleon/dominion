class BaseAgent:
    """
    Abstract base class for an agent that can play Dominion.
    """
    def __init__(self, name):
        self._name = name

    def name(self):
        """
        Returns the agents name. It should be unique for the game.
        """
        return self._name

    def make_decision(self, decision):
        """
        Return a valid choice for the decision. The choice should return True when
        passed to deicions.is_valid(choice).
        """
        raise NotImplementedError()
        