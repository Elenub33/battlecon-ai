from .fighters.fighter import Fighter

"""
An agent is any AI or human that can make choices.
The Agent class does not implement any way to make decisions and is effectively an abstract class.
"""
class Agent:
    
    
    def __init__(self, fighter: Fighter):
        self._fighter = fighter
        

    def get_fighter(self):
        return self._fighter


    def choose_attack_pair(self):
        return
    

    def choose_ante(self):
        return
    

    def choose(self, options):
        return
