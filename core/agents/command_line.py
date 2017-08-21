from core.agents.base import BaseAgent
from core.counters import CounterId
from core.counters import CounterName
from core.decision import BuyDecision
from core.locations import Location
from core.locations import LocationName


_COLORS = {
    'red': '91m'
}

def _print_color(color, msg):
    print('\x1b[%s%s\x1b[0m' % (_COLORS[color], msg))


class CommandLineAgent(BaseAgent):
    def _print_hand(self, known_state):
        print('\nYour Hand:')
        if known_state is None:
            print('Hand contents not known.')
            return
        location = Location(known_state.viewing_player, LocationName.HAND)
        info = known_state.get_location_info(location)
        print(','.join([str(card) for card in info.stack]))

    def _print_coins(self, known_state):
        if known_state is None:
            return
        num_coins = known_state.counters[CounterId(None, CounterName.COINS)]
        print('Coins: %d' % num_coins)

    def make_decision(self, decision, known_state=None):
        print('\nMake a %s decision:\n' % (decision.__class__.__name__))
        options_str = '\n'.join(
            ['%d) %s' % (i, str(opt)) for i, opt in enumerate(decision.options)]
        )
        print('Options:\n%s' % options_str)
        if isinstance(decision, BuyDecision):
            self._print_coins(known_state)
        while True:
            print('\nChoose multiple with space separated integers. Choose none by pressing enter.')
            print('\nView your hand by entering \'hand\'')
            choice = input('Enter your choice: ')
            if not choice.strip():
                return []
            if choice.strip() == '*':
                choices = decision.options
            elif choice.strip() == 'hand':
                self._print_hand(known_state)
                continue
            else:
                try:
                    choices = [decision.options[int(x)] for x in choice.split(' ')]
                except Exception:
                    _print_color('red', 'Invalid choice, failed to parse.')
                    continue
            if decision.is_valid(choices):
                return choices
            _print_color(
                'red', 'Invalid choice, choice not allowed.\n'
                'Choose between %d and %d of the options.' % (decision.min, decision.max)
            )
