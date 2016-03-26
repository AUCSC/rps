"""Simple match runner for a Rock-Paper-Scissors Tournament


Usage: 
    rps_match.py [-vd] [--games=N][--seed=S] [--agent1=AGENT1] [--agent2=AGENT2]

Options:
    -h --help
    -v                  Verbose mode, show action output messages.
    -d                  Debug mode, execute docstring tests.
    --games=N           Number of games to play [default: 7]
    --seed=S            Number to seed the random generator with.
    --agent1=AGENT1     The constructor for the Player 1 agent [default: CommandLineAgent]
    --agent2=AGENT2     The constructor for the Player 2 agent [default: CommandLineAgent]
    
"""
import agents
import random
from docopt import docopt
from datetime import datetime
import time
    
verbs = {(0, 1): "covered by",
         (0, 2): "smashes",
         (1, 0): "covers",
         (1, 2): "cut by",
         (2, 0): "smashed by",
         (2, 1): "cuts"}
         
def runner(agent1, agent2, num_trials=1, verbose=False):
    """
    Manager for a sequence of Rock-Paper-Scissors fights.
    
    Return a tuple of the wins for agent1 and agent2 out of total num_trials
    """
    w1 = 0 # wins for player 1
    w2 = 0 # wins for player 2
    
    if verbose:
        print("{} vs. {}".format(agent1, agent2))

    # run however many trials, track the wins
    for _ in range(num_trials):
        (x, y) = (agent1.act(), agent2.act())
        agent1.react(y)
        agent2.react(x)

        s = score(x, y, verbose)
        
        # record the wins
        w1 = w1 + 1 if s > 0 else w1
        w2 = w2 + 1 if s < 0 else w2
    
    # display results if necessary
    if verbose:
        winner = None
        if w1 > w2:
            winner = str(agent1)
        elif w2 > w1:
            winner = str(agent2)
        if winner:
            print("Tournament final: {}-{} with a win for {}".format(w1, w2, winner))
        else:
            print("Tournament ends with a {}-{} draw!".format(w1, w2))
    return (w1, w2)
        
def score(a1, a2, verbose=False):
    """
    Return the score for a rock-paper-scissors game.
    If verbose, display a message
    
    >>> score(Action.r, Action.r)
    0
    >>> score(Action.r, Action.r, verbose=True)
    ROCK ties ROCK: No win!
    0
    >>> score(Action.p, Action.r, True)
    PAPER covers ROCK: Player 1 wins!
    1
    >>> score(Action.s, Action.r, True)
    SCISSORS smashed by ROCK: Player 2 wins!
    -1
    >>> score(0, 1)
    -1
    """
    result = 0
    if a1 == a2:
        if verbose:
            print("{} ties {}: No win!".format(a1.name, a2.name))
        return result

    # if parity is the same, lower value wins
    if a1 % 2 == a2 % 2:
        result = 1 if a1 < a2 else -1
    else:     # if parity is different, higher value wins
        result = 1 if a1 > a2 else -1
        
    if verbose:
        winner = 1 if result > 0 else 2
        print("{} {} {}: Player {} wins!".format(a1.name,
                                                 verbs[(a1, a2)],
                                                 a2.name, 
                                                 winner))
    return result
          

def main(num_games=7, verbose=True, seed=None,
         agent1="CommandLineAgent", agent2="CommandLineAgent"):

    # double-check verbosity, if we're playing on the command line
    # we should probably tell the player what's going on
    if "CommandLine" in agent1 or "CommandLine" in agent2:
        verbose = True

    ########### Parsing arguments that might be from command line ###############
    # proper randomization - if provided properly will use as seed,
    # otherwise will generate new seed
    try:
        seed = int(seed)
    except TypeError:
        seed = int(time.mktime(datetime.now().timetuple()))

    try:
        num_games = int(num_games)
    except:
        num_games = 7

    # set up match
    random.seed(seed)
    if verbose:
        print("Starting with seed {}".format(seed))
    player1 = getattr(agents, agent1)()
    player2 = getattr(agents, agent2)()
    (w1, w2) = runner(player1, player2, num_trials=num_games, verbose=verbose)
    #TODO: save seed and player info to file here
            

if __name__ == "__main__":
    options = docopt(__doc__)
    
    # run doctests if debug flag set
    if (options['-d']):
        import doctest
        doctest.testmod()

    main(verbose=options['-v'], 
         num_games=options['--games'], 
         seed=options['--seed'],
         agent1=options['--agent1'], 
         agent2=options['--agent2'])
