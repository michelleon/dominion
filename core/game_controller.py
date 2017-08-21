import itertools
from random import sample

from core.card import CardType
from core.card_stack import UnorderedCardStack
from core.counters import CounterId
from core.counters import CounterName
from core.decision import PlayActionDecision
from core.decision import BuyDecision
from core.decision import PlayTreasureDecision
from core.game_state import GameState
from core.locations import Location
from core.locations import LocationName

from base_set.cards import GoldCard
from base_set.cards import SilverCard
from base_set.cards import CopperCard
from base_set.cards import CurseCard

from base_set.cards import EstateCard
from base_set.cards import DuchyCard
from base_set.cards import ProvinceCard

# TODO (mich):
# - implement __iter__() for card stack and distr
# - implement stubbed methods in game_controller
# - hasRandomizer on Card
STARTING_ACTION_COUNT = 1
STARTING_BUY_COUNT = 1
NUM_EMPTY_PILES_FOR_GAME_END = 3
NUM_ESTATES_IN_STARTING_HAND = 3
NUM_COPPERS_IN_STARTING_HAND = 7
NUM_CARDS_IN_HAND = 5
NUM_KINGDOM_CARDS = 10
INITIAL_SUPPLY_COUNT = 10

STARTING_VICTORY_CARD_SUPPLY_BY_PLAYER_COUNT = {
    2: 8,
    3: 12,
    4: 12,
}

STARTING_CURSE_SUPPLY_BY_PLAYER_COUNT = {
    2: 10,
    3: 20,
    4: 30,
}

STARTING_COPPER_SUPPLY = 60
STARTING_SILVER_SUPPLY = 40
STARTING_GOLD_SUPPLY = 30


class GameController(object):
    """
    The Game manages the control flow, soliciting actions from Players.
    """
    def __init__(self, players, card_set, log):
        self.players = players # array of agents
        self.num_players = len(players)
        # all agents need to implement a .name() method
        self.game_state = None
        # Array of cards that kingdom will be chosen from
        self.card_set = card_set
        # Player index = index of player whose turn it is 
        self.player_index = 0 # TODO: randomize start player
        self.starting_player_index = self.player_index
        self.log = log


    def get_starting_supply(self):
        """
        - choose 10 kingdom cards from card_set
        - initialize victory card supply
        - initalize treasure supply
        - initialize curse supply if Witch in play
        """
        # TODO cards need hasRandomizer method
        randomizer_cards = [x for x in self.card_set if x.hasRandomizer()]
        num_to_sample = min(NUM_KINGDOM_CARDS, len(self.card_set))
        kingdom_cards = sample(randomizer_cards, num_to_sample) * INITIAL_SUPPLY_COUNT
        treasure_cards = (
            [GoldCard] * STARTING_GOLD_SUPPLY +
            [SilverCard] * STARTING_SILVER_SUPPLY +
            [CopperCard] * STARTING_COPPER_SUPPLY
        )

        victory_starting_supply = STARTING_VICTORY_CARD_SUPPLY_BY_PLAYER_COUNT[self.num_players]
        victory_cards = [[card] * victory_starting_supply for card in [EstateCard, DuchyCard, ProvinceCard]]
        flattened_victory_cards = list(itertools.chain.from_iterable(victory_cards))

        curse_starting_supply = STARTING_CURSE_SUPPLY_BY_PLAYER_COUNT[self.num_players]
        curse_cards = [CurseCard] * curse_starting_supply
        # TODO: how to handle gardens etc. which depend on num_players
        return UnorderedCardStack(kingdom_cards + treasure_cards + flattened_victory_cards)

    def get_starting_deck(self):
        return (
            [CopperCard] * NUM_COPPERS_IN_STARTING_HAND +
            [EstateCard] * NUM_ESTATES_IN_STARTING_HAND
        )

    def _increment_player_index(self, index):
        next_index = (index + 1) % self.num_players
        return next_index

    def next_player_index(self):
        next_player = self._increment_player_index(self.player_index)
        self.game_state._current_player_index = next_player
        return next_player

    def actions_left(self):
        return self.game_state.get_counter(CounterId(None, CounterName.ACTIONS))

    def buys_left(self):
        return self.game_state.get_counter(CounterId(None, CounterName.BUYS))

    def money_in_play(self):
        return self.game_state.get_counter(CounterId(None, CounterName.COINS))

    def action_cards_in_hand(self, player):
        hand = self.game_state.get_location(Location(player.name(), LocationName.HAND))
        return [card for card in hand if CardType.ACTION in card.types]

    def game_over(self):
        supply = self.game_state.get_location(Location(None, LocationName.SUPPLY))
        if supply.distribution.count(ProvinceCard) == 0:
            return True
        cards_to_counts = supply.distribution.cards_to_counts()
        if list(cards_to_counts.values()).count(0) >= 3:
            return True
        return False

    def generate_buy_decision(self, player):
        """
        Params:
          player: Player agent object

        Returns:
            BuyDecision with options being all the available
            supply cards that the player can afford
        """
        money = self.money_in_play()
        available_cards = set(list(self.game_state.get_location(Location(None, LocationName.SUPPLY))))
        affordable_cards = [card for card in available_cards if card.cost(self.game_state) <= money]
        return BuyDecision(options=affordable_cards, min=0, max=1)

    def generate_action_decision(self, player):
        """
        Params:
          player: Player agent object

        Returns:
            PlayActionDecision with options being all action cards in player's hand
        """
        return PlayActionDecision(options=self.action_cards_in_hand(player), min=0, max=1)

    def generate_play_treasures_decision(self, player):
        """
        Params:
          player: Player agent object

        Returns:
            PlayTreasureDecision with options being all treasure cards in player's hand
        """
        hand_stack = self.game_state.get_location(Location(player.name(), LocationName.HAND))
        treasures_in_hand = [card for card in hand_stack if CardType.TREASURE in card.types]
        return PlayTreasureDecision(options=treasures_in_hand, min=0, max=len(treasures_in_hand))

    def take_buy_action(self, player, card):
        """
        Params:
          player_name: string
          card: Card class

        Moves card from supply to player discard pile
        """
        cost = card.cost(self.game_state)
        self.game_state.update_counter(CounterId(None, CounterName.BUYS), -1)
        self.game_state.update_counter(CounterId(None, CounterName.COINS), 0 - cost)
        self.game_state.gain(card)

    def play_treasures(self, player, treasures):
        """
        Params:
          player_name: string
          treasures: array of Card class, must all be treasure type cards

        Moves cards from HAND to IN_PLAY
        Increments COINS counter by the sum of `treasures`
        """
        for treasure in treasures:
            self.game_state.play(treasure)
            treasure.play(self.game_state)

    def player_name_to_vp(self):
        """
        Counts up all players victory points
        Returns: map of player name to VP
        """
        player_name_to_vp = {}
        for player_name in list(map(lambda p: p.name(), self.players)):
            deck = self.game_state.get_deck(player_name)
            victory_points = sum([card.victory_points(player_name, self.game_state) for card in deck])
            player_name_to_vp[player_name] = victory_points
        return player_name_to_vp

    def get_winner_indices(self, start_turn_index, next_turn_index, scores):
        """
        Returns a list of the indices of the winning players. There can be multiple if there is a tie.

        Parameters:
            start_turn_index (int): The index of the player that started first.
            next_turn_index (int): The index of the player whose turn would be next if the game
                wasn't over.
            scores (list of int): The final score for each player. The score at index i is the
                score for the player at index i.
        """
        top_score = max(scores)
        cur_index = next_turn_index
        players_have_one_less_turn = True
        winners = []
        while True:
            if cur_index == start_turn_index:
                if winners:
                    return winners
                players_have_one_less_turn = False
            if scores[cur_index] == top_score:
                winners.append(cur_index)
            cur_index = self._increment_player_index(cur_index)
            if cur_index == next_turn_index:
                break
        return winners

    def get_winners(self):
        """
        Returns a list of the winning player names.
        """
        player_name_to_vp = self.player_name_to_vp()
        scores = []
        for player in self.players:
            scores.append(player_name_to_vp[player.name()])
        winner_indices = self.get_winner_indices(
            self.starting_player_index, self.player_index, scores
        )
        winners = [self.players[ind].name() for ind in winner_indices]
        return winners

    def run(self):
        """
        Main control loop for game play
        """
        #################
        # Initialization
        #################

        starting_supply = self.get_starting_supply()
        starting_deck = self.get_starting_deck()
        self.game_state = GameState(
            list(map(lambda x: x.name(), self.players)),
            starting_supply,
            starting_deck,
            self.log
        )
        # TODO: inform Players of initial state for learning agents
        self.game_state.set_agents(self.players)
        for player in self.players:
            # shuffle player decks
            self.game_state.shuffle(Location(player.name(), LocationName.DRAW_PILE))
            # draw starting hands
            self.game_state.draw(NUM_CARDS_IN_HAND, player.name())

        #################
        # Gameplay loop
        #################
        turn_number = 1
        while not self.game_over():
            # Fetch the next player
            player = self.players[self.player_index]
            ### Setup Phase
            self.game_state.reset_counters_for_new_turn()

            ### Action phase

            while (
                self.actions_left() > 0 and
                len(self.action_cards_in_hand(player)) > 0
            ):
                decision = self.generate_action_decision(player)
                choices = player.make_decision(decision)
                action_card = choices[0] if choices else None
                # TODO: validate choice legality
                if not action_card:
                    break
                self.game_state.update_counter(CounterId(None, CounterName.ACTIONS), -1)
                self.game_state.play(action_card)
                action_card.play(self.game_state)

            ### Buy phase
            decision = self.generate_play_treasures_decision(player)
            treasures = player.make_decision(decision) # expect choice to be arr of treasure cards
            self.play_treasures(player, treasures)

            while self.buys_left() > 0:
                decision = self.generate_buy_decision(player)
                choices = player.make_decision(decision)
                choice = choices[0] if choices else None
                # TODO: validate choice legality
                if not choice:
                    break
                self.take_buy_action(player, choice)
            
            ### Discard cards in play and in hand
            self.game_state.discard_location(Location(player.name(), LocationName.IN_PLAY))
            self.game_state.discard_location(Location(player.name(), LocationName.HAND))

            ### Draw next hand
            self.game_state.draw(NUM_CARDS_IN_HAND, player.name())

            # TODO: inform Players of after turn state for learning agents
            
            # rotate player index
            self.player_index = self.next_player_index()
            turn_number += 1

        #################
        # Resolve game
        #################
        print('\nGAME OVER on Turn %d\n-----------------\n' % (turn_number / 2))
        for name, vp in self.player_name_to_vp().items():
            print('%s: %d' % (name, vp))
        winners = self.get_winners()
        if len(winners) == 1:
            print('Winner: ' + winners[0])
        elif len(winners) == 2:
            tied_player_names = ' and '.join(winners)
            print('Tie between %s' % tied_player_names)
        return winners




