# dominion
[![CircleCI](https://circleci.com/gh/michelleon/dominion.svg?style=svg)](https://circleci.com/gh/michelleon/dominion)

## Requirements
- python 3.4.6+

## Quick Start
First make sure the project directory is in your python path
```
export PYTHONPATH="${PYTHONPATH}:/path/to/dominion/"
```
To run a game use the play.py script. Choose the `CommandLineAgent` for a human player.
```
python3 play.py --p1 core.agents.command_line.CommandLineAgent
```

Every time you are required to make a decision during the game you will be presented with a decision name and a list of options. Choose the options by entering space separated integers corresponding to their index in the list.

If you enter `*` it will choose all the options. This is useful for playing all your treasures instead of typing out the index of each one.
