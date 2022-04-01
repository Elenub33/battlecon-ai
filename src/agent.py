import src.fighters.fighter as fighter

"""
An agent is any AI or human that can make choices.
The Agent class does not implement any way to make decisions and is effectively an abstract class.
"""
class Agent:
    
    
    def __init__(self, fighter: fighter.Fighter):
        self.fighter = fighter
        
        
    def get_fighter(self):
        return self.fighter