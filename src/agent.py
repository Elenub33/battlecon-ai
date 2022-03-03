import fighters

"""
An agent is any AI or human that can make choices.
Agent itself is intended to be overridden and embellished by subclasses.
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
        self.fighter = fighters.character_dict[self.fighter_name.lower()](self.get_game(), self.get_player_number(), base_set=self.bases, is_user=self.is_human())
        self.fighter.set_agent(self)
        
        
    def __str__(self):
        return self.get_name()
        
    
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
    ------------ Wrappers for fighter behavior. ------------
    Ultimate goal here is:
    1. find and isolate the decision making code
    2. force the decision making code to pass through the agent class to get to the fighter
    3. refactor so the agent is making the decisions, not the fighter
    
    Possible complication: a lot of the logic happens in battlecon.py, directly using information from fighters.py.
    The plan might need to be more nuanced than this.
    See:
    * the existence of player.set_chosen_strategy(strat)
    
    
    It might just be as simple as this: somewhere, there's a state evaluation function. evaluate() maybe? If I change that function to be based on reinforcement learning, does the rest just fall into place?
    
    
    also: look for is_user (especially in fighters.py) or self.interactive in battlecon.py for locations where decisions are made.
    """
    # TODO: in this section especially, pull AI and human logic out of the fighters and into the Yaron/Human agents
    
    
    """
    Agent saves the opponent's agent as opponent, fighter and cards save the opponent's fighter as opponent.
    """
    def set_opponent(self, opponent):
        self.opponent = opponent
        my_fighter, opp_fighter = self.get_fighter(), opponent.get_fighter()
        my_fighter.opponent = opp_fighter
        for card in my_fighter.all_cards():
            card.opponent = opp_fighter
        
    
    def select_finisher(self):
        self.get_fighter().select_finisher()
        
    
    def get_strategy_name(self, strategy):
        return self.get_fighter().get_strategy_name(strategy)
        
    
    def initial_save(self):
        return self.get_fighter().initial_save()
        
    
    def initial_restore(self, state):
        self.get_fighter().initial_restore(state)
        
    
    def full_save(self):
        return self.get_fighter().full_save()
        
        
    def full_restore(self, state):
        self.get_fighter().full_restore(state)
        
        
    def reset(self):
        self.get_fighter().reset()
        
        
    def get_all_possible_strategies(self):
        return self.get_fighter().get_strategies()
        
        
    """
    Replacement for player.strat in the Yaron version.
    """
    def get_chosen_strategy(self):
        return self.get_fighter().strat
        
        
    def set_chosen_strategy(self, strat):
        self.get_fighter().strat = strat
        
        
    def get_chosen_strategy_name(self):
        return self.get_strategy_name(self.get_chosen_strategy())
        
        
    def get_name(self):
        return self.get_fighter().name
        
        
    def choose_finisher_base_retroactively(self):
        return self.get_fighter().choose_finisher_base_retroactively()
        
        
    def wins_on_timeout(self):
        return self.get_fighter().wins_on_timeout()
        
    
    def set_preferred_range(self):
        self.get_fighter().set_preferred_range()
        
    
    def get_preferred_range(self):
        return self.get_fighter().preferred_range
        
        
    def evaluate_superposition(self):
        return self.get_fighter().evaluate_superposition()
        
        
    def evaluate_range(self):
        return self.get_fighter().evaluate_range(self)
        
        
    def evaluate(self):
        return self.get_fighter().evaluate()
        
    
    def input_pre_attack_decision_index(self):
        return self.get_fighter().input_pre_attack_decision_index()
        
        
    # TODO: don't forward this to fighter; calculate at the agent level
    def choose_strategy(self, limit_antes=False):
        return self.get_fighter().choose_strategy(limit_antes)