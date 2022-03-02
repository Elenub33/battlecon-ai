import fighters

"""
An agent is any AI or human that can make choices.
Agent itself is abstract.
"""
class Agent:
    

    """
    Create the agent object. Note that this is only the first part of setup; the second part occurs during initialize_game.
    """
    def __init__(self, fighter_name, bases="alpha"):
        self.game = None
        self.player_number = None
        self.fighter = None
        self.fighter_name = fighter_name
        self.bases = bases
        
    
    """
    Instantiate the fighter, 
    """
    def initialize_game(self, game, player_number):
        self.game = game
        self.player_number = player_number
        self._create_fighter()
        
    
    """
    Instantiate a new fighter for this agent using the fighter name and properties of the agent.
    This should only be called from initialize_game.
    """
    def _create_fighter(self):
        self.fighter = fighters.character_dict[self.fighter_name.lower()](self.get_game(), self.get_player_number(), self.bases, is_user=self.is_human())
        
    
    """
    This is a transitional method used to replace the is_user flag in fighter.Character.
    """
    def is_human(self):
        return False
    
    
    """
    Return the fighter played by this agent.
    """
    def get_fighter(self):
        return self.fighter
    
    
    """
    Return the agent's game.
    """
    def get_game(self):
        return self.game
    
    
    """
    Return the agent's game.
    """
    def get_player_number(self):
        return self.player_number
        
        
    """
    ---- Wrappers for fighter methods. ----
    """
    # TODO: pull AI and human logic out of the fighters and into the Yaron/Human agents
    # def evaluate(self):
    