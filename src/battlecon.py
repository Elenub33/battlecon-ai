#!/usr/bin/env python3
import random
import agent, fighter
    

class Game:


    def __init__(self, agent0, agent1):
        assert isinstance(agent0, agent.Agent)
        assert isinstance(agent1, agent.Agent)
        self.agents = [agent0, agent1]
        self.state = GameState(agent0.get_fighter(), agent1.get_fighter())
    
    
    def initialize_from_start(self):
        self.state.initialize_from_start()
    
    
    def initialize_from_file(self):
        raise NotImplementedError()
    
    
    def get_active_agent(self):
        active_fighter = self.state.get_active_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find active agent.")
    
    
    def get_reactive_agent(self):
        active_fighter = self.state.get_reactive_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find reactive agent.")
    
    
    def get_state(self):
        return self.state
        
        
    def execute_beat(self):
        pass
        
        
"""
All state accessor and mutation methods should be on the GameState class.
The main state and possible future states are passed to agents to help them analyze and make decisions.
"""
class GameState:


    def __init__(self, fighter0: fighter.Fighter, fighter1: fighter.Fighter):
        self.set_beat_state(SetPairs(self))
        self.fighters = [fighter0, fighter1]
        self.fighter_states = {}
        self.fighter_states[fighter0] = fighter.FighterState(fighter0)
        self.fighter_states[fighter1] = fighter.FighterState(fighter1)
        self.active_fighter_index = 0
    
    
    def initialize_from_start(self):
        self.active_fighter_index = random.randint(0, 1)
        
        
    def get_beat_state(self) -> 'BeatState':
        return self.beat_state
        
    
    def get_active_fighter(self) -> fighter.Fighter:
        return self.fighters[self.active_fighter_index]
        
    
    def get_reactive_fighter(self) -> fighter.Fighter:
        return self.fighters[1 - self.active_fighter_index]
        
    
    def get_active_fighter_state(self) -> fighter.FighterState:
        return self.get_fighter_state(self.get_active_fighter())
        
    
    def get_reactive_fighter_state(self) -> fighter.FighterState:
        return self.get_fighter_state(self.get_reactive_fighter())
        
        
    def get_fighter_state(self, fighter: fighter.Fighter) -> fighter.FighterState:
        return self.fighter_states[fighter]
        
        
    def process_beat_state(self):
        self.get_beat_state().handle()
        self.advance_beat_state()
        
    
    def set_beat_state(self, state: 'BeatState'):
        self.beat_state = state
        
        
    def advance_beat_state(self):
        self.set_beat_state(self.get_beat_state().get_next())
        
        
    def set_fighter_strategy(self, fighter, strategy):
        self.get_fighter_state(fighter).set_attack_strategy(strategy)
        
        
    def set_fighter_position(self, fighter, position):
        self.get_fighter_state(fighter).set_position(position)
        
    
    def get_distance_between_fighters(self):
        return abs(self.get_active_fighter_state().get_position() - self.get_reactive_fighter_state().get_position())
        


class BeatState:


    def __init__(self, game_state: 'GameState'):
        self.game_state = game_state
        
        
    def get_game_state(self):
        return self.game_state
        
        
    def handle(self):
        pass
        
        
    def get_next(self) -> 'BeatState':
        return self.get_next_state_class()(self.get_game_state())
        
        
    def get_next_state_class(self) -> type:
        raise NotImplementedError()
        
        
class SetPairs(BeatState):
    def get_next_state_class(self) -> type:
        return SetAntes
    
    
class SetAntes(BeatState):
    def get_next_state_class(self) -> type:
        return Reveal
    
    
class Reveal(BeatState):
    def get_next_state_class(self) -> type:
        return CheckForClash
    
    
class CheckForClash(BeatState):
    def get_next_state_class(self) -> type:
        return StartOfBeat
    
    
class StartOfBeat(BeatState):
    def get_next_state_class(self) -> type:
        return ActiveBefore
    
    
class ActiveBefore(BeatState):
    def get_next_state_class(self) -> type:
        return ActiveCheckRange
            
    
class ActiveCheckRange(BeatState):
    def get_next_state_class(self) -> type:
        range = self.get_game_state().get_active_fighter_state().get_attack_strategy().get_range()
        distance = self.get_game_state().get_distance_between_fighters()
        print(range)
        if range[0] >= distance and range[1] <= distance:
            return ActiveHit
        else:
            return ActiveAfter
            
    
class ActiveHit(BeatState):
    def get_next_state_class(self) -> type:
        return ActiveDamage
            
    
class ActiveDamage(BeatState):
    pass
            
    
class ActiveAfter(BeatState):
    pass