from random import choice

# Number of unique card types to start the game with in the supply.
# Does not include the always presents cards like Copper, Estate, etc.
NUMBER_OF_CARDS_IN_KINGDOM = 10
STARTING_HAND_SIZE = 5
# Put cards that are in every game regardless of the kingdom randomization
DEFAULT_SUPPLY_CARDS = []

class GameController(object):
    def __init__(self):
        self._game_state = None

    def choose_kingdom(self, allowed_cards, num_players):
        chosen = []
        choices = allowed_cards[:]
        dist = CardDistribution()
        for i in xrange(NUMBER_OF_CARDS_IN_KINGDOM):
            card = choice(choices)
            choices.remove(card)
            dist.add(card, card.get_starting_pile_size(num_players))
        for card in DEFAULT_SUPPLY_CARDS:
            dist.add(card, card.get_starting_pile_size(num_players))
        return dist

    def new_game(self, player_names, clients, allowed_cards=None):
        supply = self.choose_kingdom(allowed_cards, len(player_names))
        self._game_state = GameState(player_names, supply)
        self._clients = clients
        # Draw initial hands
        for name in player_names:
            DrawCardsInstruction.execute(self._game_state, name, STARTING_HAND_SIZE)
        self.run_game()

    def run_game(self):
        while True:
            action_to_player = self._game_state.action_to_player
            if self.next_action_
            player = self._clients[action_to_player]
            player.take_action(self._game_state.view_as(player))



class Card(object):
    @staticmethod
    def get_starting_pile_size(num_players):
        return 10

# Add a number parameter to CardDistribution.add