from core.agents.base import BaseAgent

_COLORS = {
    'red': '91m'
}

def _print_color(color, msg):
    print('\x1b[%s%s\x1b[0m' % (_COLORS[color], msg))


class CommandLineAgent(BaseAgent):
    def make_decision(self, decision):
        print('\nMake a %s decision:\n' % (decision.__class__.__name__))
        options_str = '\n'.join(
            ['%d) %s' % (i, str(opt)) for i, opt in enumerate(decision.options)]
        )
        print('Options:\n%s' % options_str)
        while True:
            print('\nChoose multiple with space separated integers. Choose none by pressing enter.')
            choice = input('Enter your choice: ')
            if not choice.strip():
                return []
            if choice.strip() == '*':
                choices = decision.options
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
