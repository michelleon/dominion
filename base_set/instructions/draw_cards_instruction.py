from core.instruction import Instruction


class DrawCardsInstruction(Instruction):
    """
    Draws cards for the target player. If their draw pile is empty before all the cards are
    drawn then their discard pile is shuffled into their draw pile and the drawing continues.
    If the discard pile is also empty then no more cards are drawn.

    All drawn cards end up in the players hand.
    """
    def __init__(self, number_to_draw, target_player):
        self.number_to_draw = number_to_draw
        self.target_player = target_player

    def execute(self, game_state, logger):
        player_state = game_state.get_player_state(self.target_player)
        number_left_to_draw = self.number_to_draw
        cards = []
        while True:
            drawn_cards = player_state.draw_pile.draw(number_left_to_draw)
            logger.info('%s drew %d cards.' % (self.target_player, len(drawn_cards)))
            cards.extend(drawn_cards)
            if len(cards) == self.number_to_draw:
                break
            logger.info('No cards left in draw pile.')
            number_left_to_draw = self.number_to_draw - len(cards)
            if player_state.discard.is_empty():
                logger.info('No cards left in discard pile.')
                break
            logger.info('Shuffling discard pile into draw pile to continue drawing.')
            player_state.draw_pile = player_state.discard.deepcopy()
            player_state.draw_pile.shuffle()
            player_state.discard.empty()
        for card in cards:
            player_state.hand.add(card)
