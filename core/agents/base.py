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

    def make_decision(self, decision, known_state=None):
        """
        Return a valid choice for the decision. The choice should return True when
        passed to deicions.is_valid(choice).

        Parameters:
            decicion (`Decision`): The decision to be made.
            known_state (optional, `ViewableGameState`): The state known at the time of the
                decision.
        """
        raise NotImplementedError()
        