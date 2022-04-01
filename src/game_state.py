#!/usr/bin/env python3
import random
import src.agent as agent, src.fighters.fighter as fighter

"""
All state accessor and mutation methods should be on the GameState class.
The main state and possible future states are passed to agents to help them analyze and make decisions.
This class contains no agents or other information that could lead to deduction of opponent strategy.
"""
class GameState:


    @staticmethod
    def from_start(fighter0: fighter.Fighter, fighter1: fighter.Fighter):
        state = GameState(fighter0, fighter1)
        state.initialize_from_start()
        return state


    def __init__(self, fighter0: fighter.Fighter, fighter1: fighter.Fighter):
        self.fighters = [fighter0, fighter1]
        self.fighter_states = {}
        self.fighter_states[fighter0] = fighter.FighterState(fighter0)
        self.fighter_states[fighter1] = fighter.FighterState(fighter1)
        self.set_active_fighter(None)
    
    
    def initialize_from_start(self):
        self.set_active_fighter(random.choice(self.fighters))
        self.get_active_fighter_state().set_position(2)
        self.get_reactive_fighter_state().set_position(4)
        
    
    def set_active_fighter(self, fighter: fighter.Fighter):
        self.active_fighter = fighter
    
    
    def get_active_fighter(self) -> fighter.Fighter:
        if not self.active_fighter:
            raise Exception("Unable to find active fighter.")
        return self.active_fighter
        
    
    def get_reactive_fighter(self) -> fighter.Fighter:
        if not self.active_fighter:
            raise Exception("Unable to find reactive fighter. Active fighter not set.")
        for f in self.fighters:
            if f is not self.active_fighter:
                return f
        raise Exception("Unable to find reactive fighter. Active fighter set, but no other fighter exists.")
        
    
    def get_active_fighter_state(self) -> fighter.FighterState:
        return self.get_fighter_state(self.get_active_fighter())
        
    
    def get_reactive_fighter_state(self) -> fighter.FighterState:
        return self.get_fighter_state(self.get_reactive_fighter())
        
        
    def get_fighter_state(self, fighter: fighter.Fighter) -> fighter.FighterState:
        return self.fighter_states[fighter]
        
        
    def clear_fighter_positions(self):
        for fighter in self.fighters:
            self.get_fighter_state(fighter).set_position(-1)
        
        
    def set_fighter_position(self, fighter, position):
        for f in self.fighters:
            if f is not fighter and self.get_fighter_state(f).get_position() == position:
                raise Exception("Unable to move {} to position {}: already occupied by {}.".format(fighter, position, f))
        self.get_fighter_state(fighter).set_position(position)
        
    
    def get_distance_between_fighters(self):
        return abs(self.get_active_fighter_state().get_position() - self.get_reactive_fighter_state().get_position())