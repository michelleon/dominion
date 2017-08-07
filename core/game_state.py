from collections import deque

from core.card_distribution import CardDistribution
from core.card_stack import CardStack
from core.player_state import PlayerState


class GameState(object):
    """
    Contains all global game state.
    """
    def __init__(self, player_names, supply, starting_cards):
        """
        Parameters:
            player_names (list of `str`): List of player names in the order of their turns.
            supply (CardDistribution): All cards in the global supply.
            starting_cards (list of `Card`): The cards that each player will start with in their
                deck.
        """
        self.player_names = tuple(player_names)
        self._player_states = GameState._create_initial_player_states(player_names, starting_cards)
        self.trash = CardDistribution()
        self.supply = CardDistribution()
        self._current_turn = 0
        self._action_to_player = 0
        # Next choice that needs to be made by the player indicated by self._action_to_player
        self._current_choice = None
        # A stack of events to be resolved in order
        self._event_stack = deque()
        # All events that have already been resolved this turn.
        self._resolved_events = deque()

    @staticmethod
    def _create_initial_player_states(player_names, starting_cards):
        player_states = {}
        for name in player_names:
            player_states[name] = PlayerState(name=name, starting_cards=starting_cards)
        return player_states

    def deepcopy(self):
        """
        Return a copy of the GameState that can be mutated without changing the GameState.
        """
        new_state = GameState(player_names=[])
        new_state.player_names = self.player_names
        copied_player_states = {}
        for name, state in self._player_states.iteritems():
            copied_player_states[name] = state.deepcopy()
        new_state.trash = self.trash.deepcopy()
        new_state.supply = self.supply.deepcopy()
        new_state._current_turn = self._current_turn
        new_state._current_choice = self._current_choice.deepcopy()
        new_state._action_to_player = self._action_to_player
        new_state._event_stack = deque(self._event_stack[:])
        new_state._resolved_events = deque(self._resolved_events[:])
        return new_state

    def get_player_state(self, player_name):
        return self._player_states[player_name]

    def view_as(self, player_name):
        """
        Return a GameState that the player with player_name is aware of. Hides any state that the player is not aware of.
        """
        raise NotImplementedError()



