"""Simple experiment runner for a Rock-Paper-Scissors Tournament.

Will have to import all the agent libraries, and then
"""
from rps_match import *

import agents # import default agent library
# import tournament agent libraries

# specify the agents to actually run in the tournament
agents = ['agents.NashAgent', 'agents.StubbornAgent', 
          'agents.MirrorAgent', 'agents.CounterAgent']

num_games = 10000
time_limit = 36000 # ten minutes per match

# TODO: all the stuff to make this work
# TODO: figure out how to handle slow agents (remove from results? count as losses?)
# TODO: submit jobs 
# TODO: save results files for each pair with seed
# TODO: dynamically load agents
