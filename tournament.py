"""Simple experiment runner for a Rock-Paper-Scissors Tournament"""
from agents import *
    
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
        
        # recore the wins
        w1 = w1 + 1 if s > 0 else w1
        w2 = w2 + 1 if s < 0 else w2
    
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
          



if __name__ == "__main__":
    agent1 = CounterAgent()
    agent2 = CounterAgent()
    runner(agent1, agent2, 5, verbose=True)