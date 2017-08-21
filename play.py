import argparse

from base_set.cards import KINGDOM_CARDS
from core.game_controller import GameController
from core.loggers.human import HumanReadableLogger


def play_game(p1_agent, p2_agent):
	controller = GameController(
	    players=[p1_agent, p2_agent],
	    card_set=KINGDOM_CARDS,
	    log=HumanReadableLogger()
	)
	controller.run()


def _str_to_agent_class(s):
	parts = s.split('.')
	klass = parts[-1]
	module_str = '.'.join(parts[:-1])
	module = __import__(module_str, fromlist=[klass])
	klass_obj = getattr(module, klass)
	return klass_obj


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--p1", help="Full path to agent to play as player 1")
	parser.add_argument("--p2", help="Full path to agent to play as player 2")
	args = parser.parse_args()
	p1_path = args.p1 or 'core.agents.big_money.SimpleBmSmithyAgent'
	p1_agent = _str_to_agent_class(p1_path)('p1')
	p2_path = args.p2 or 'core.agents.big_money.SimpleBmSmithyAgent'
	p2_agent = _str_to_agent_class(p2_path)('p2')
	play_game(p1_agent, p2_agent)