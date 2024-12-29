import random
from .fighters.fighter import Fighter, FighterState

"""
A GameState object tracks the state of the board fighters. It does not track phase state information; see game_phases.py.

This class contains no agents or other information that could lead to deduction of opponent strategy.
"""
class GameState:


    @staticmethod
    def from_start(fighter0: Fighter, fighter1: Fighter):
        state = GameState(fighter0, fighter1)
        state.initialize_from_start()
        return state


    def __init__(self, fighter0: Fighter, fighter1: Fighter):
        self._fighters = [fighter0, fighter1]
        self._fighter_states = {}
        self._fighter_states[fighter0] = FighterState(fighter0)
        self._fighter_states[fighter1] = FighterState(fighter1)
        self.set_force_pool(0)
        self.set_active_fighter(None)


    # is_over returns true if the game is over.
    def is_over(self):
        return self.get_force_pool() <= 0 or self.get_active_fighter_state().get_life() <= 0 or self.get_reactive_fighter_state().get_life() <= 0
    
    
    def initialize_from_start(self):
        self.set_active_fighter(random.choice(self._fighters))
        self.get_active_fighter_state().set_position(2)
        self.get_reactive_fighter_state().set_position(4)
        self.set_force_pool(41)
        

    def set_force_pool(self, force_pool: int):
        self._force_pool = force_pool

    
    def get_force_pool(self) -> int:
        return self._force_pool

    
    def set_active_fighter(self, fighter: Fighter):
        self._active_fighter = fighter
    
    
    def get_active_fighter(self) -> Fighter:
        if not self._active_fighter:
            raise Exception("Unable to find active fighter.")
        return self._active_fighter
        
    
    def get_reactive_fighter(self) -> Fighter:
        if not self._active_fighter:
            raise Exception("Unable to find reactive fighter. Active fighter not set.")
        for f in self._fighters:
            if f is not self._active_fighter:
                return f
        raise Exception("Unable to find reactive fighter. Active fighter set, but no other fighter exists.")
        
    
    def get_active_fighter_state(self) -> FighterState:
        return self.get_fighter_state(self.get_active_fighter())
        
    
    def get_reactive_fighter_state(self) -> FighterState:
        return self.get_fighter_state(self.get_reactive_fighter())
        
        
    def get_fighter_state(self, fighter: Fighter) -> FighterState:
        return self._fighter_states[fighter]
        
        
    def clear_fighter_positions(self):
        for fighter in self._fighters:
            self.get_fighter_state(fighter).set_position(-1)
        
        
    def set_fighter_position(self, fighter, position):
        for f in self._fighters:
            if f is not fighter and self.get_fighter_state(f).get_position() == position:
                raise Exception("Unable to move {} to position {}: already occupied by {}.".format(fighter, position, f))
        self.get_fighter_state(fighter).set_position(position)
        
    
    def get_distance_between_fighters(self):
        return abs(self.get_active_fighter_state().get_position() - self.get_reactive_fighter_state().get_position())