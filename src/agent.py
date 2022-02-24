"""
An agent is any AI or human that can make choices.
Agent itself is abstract.
"""
class Agent:
    
    
    """
    This is a transitional method used to replace the is_user flag in fighter.Character.
    """
    def isHuman(self):
        return False
        
        
"""
Yaron's original AI.
"""
class YaronAgent(Agent):
    
    pass

"""
A human player.
"""
class HumanAgent(Agent):
    
    def isHuman(self):
        return True