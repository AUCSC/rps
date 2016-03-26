import random
from enum import IntEnum
from contextlib import suppress

class Action(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2
    # aliases
    r = 0
    p = 1
    s = 2
    R = 0
    P = 1
    S = 2
    rock = 0
    paper = 1
    scissors = 2

class RPSAgent():
    """
    Interface for a generic Rock-Paper-Scissors agent.
    """
    
    def __init__(self):
        """
        Whatever setup you might need to do for a match, do here.
        """
        pass
    
    def act(self):
        """
        And however you might want to act, do it here.
        Must return an Action.
        """
        return Action.r
    
    def react(self, response):
        """
        And respond however you would like to the action taken by 
        the other player. Nothing returned.
        """
        pass
    
    def __str__(self):
        """
        Return a nicely formatted name
        """
        return self.__class__.__name__
          
    
class CommandLineAgent(RPSAgent):
    """
    Allows humans to play in the bot tournaments. Prompts user for action 
    selection at each round. Does not cheat.
    """
    def __init__(self, actions="[r]ock, [p]aper, [s]cissors"):
        self.actions = actions
        pass

        
    def act(self):
        choice = None
        while choice is None:
            choice = input("Select action {}: ".format(self.actions))
            try:
                choice = Action[choice]
            except KeyError:
                # one last try
                with suppress(ValueError):
                    choice = Action(int(choice))
                    return choice
                
                # okay, this is not a choice
                print("{} is not a valid action".format(choice))
                choice = None
        return choice

    
class StubbornAgent(RPSAgent):
    """
    Choose an action at the start and stick to it.
    """
    def __init__(self, action=None):
        if action is None:
            action = random.choice(list(Action))
        self.action = action
            
    def act(self):
        return self.action

    
class NashAgent(RPSAgent):
    """
    Uniformly randomly choose an action each time, ignoring
    opponent actions.
    """
    def __init__(self):
        self.actions = list(Action)
    
    def act(self):
        return random.choice(self.actions)
        

class MirrorAgent(RPSAgent):
    """
    Randomly choose your first action, then always choose the action
    the opponent chose last time
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        
    def act(self):
        return self.action

    def react(self, response):
        self.action = response

class CounterAgent(RPSAgent):
    """
    Randomly choose your first action, then always choose the next action
    that would have beaten the opponent's last action
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        
    def act(self):
        return self.action
    
    def react(self, response):
        action = (response + 1) % len(Action)
        self.action = Action(action)
        
class SelfCounterAgent(RPSAgent):
    """
    Randomly choose your first action, then always choose the next action
    that would have beaten your last action
    """
    def __init__(self):
        self.action = random.choice(list(Action))
        
    def act(self):
        return self.action
    
    def react(self, response):
        response = (self.action + 1) % len(Action)
        self.action = Action(response)
    
       
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Done tests")
    