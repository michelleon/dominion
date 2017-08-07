class Instruction(object):
    """
    Base class for all Instructions.

    An Instruction contains logic for changing the game state. It has an execute method which
    takes a game state and returns the mutated game state after executing the instruction.
    """
    def execute(self, game_state, logger):
        """
        Return mutated game_state after executing the instruction.

        Parameters:
            game_state (`GameState`): The game state to execute the instruction on.
            logger (`Logger`): An instance of `Logger` to write any information about the execution to.
        """
        raise NotImplementedError()



class NoOpInstruction(Instruction):
    def execute(self, game_state, logger):
        return game_state
