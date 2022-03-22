#!/usr/bin/env python3
import random
import agent
    

class Game:


    def __init__(self, agent0, agent1):
        assert isinstance(agent0, agent.Agent)
        assert isinstance(agent1, agent.Agent)
        self.agents = [agent0, agent1]
        # self.fighters = [agent0.get_fighter(), agent1.get_fighter()]
    
    
    def initialize_from_start(self):
        self.active_player = random.choice(self.agents)
    
    
    def initialize_from_file(self):
        raise NotImplementedError()
    
    
    def get_active_player(self):
        return self.active_player
    
    
    def get_reactive_player(self):
        for agent in self.agents:
            if agent != self.active_player:
                return agent
    
    
    def get_state(self):
        return GameState()
        
        
    def execute_beat(self):
        pass
        
        
        
        
"""
All state accessor and mutation methods should be on the GameState class.
The main state and possible future states are passed to agents to help them analyze and make decisions.
"""
class GameState:

    def __init__(self):
        self.set_beat_state(SetPairs(self))
        
        
    def get_beat_state(self) -> 'BeatState':
        return self.beat_state
        
        
    def set_beat_state(self, state: 'BeatState'):
        self.beat_state = state
        
        
    def process_beat_state(self):
        self.get_beat_state().process()
        self.advance_beat_state()
        
        
    def advance_beat_state(self):
        self.set_beat_state(self.get_beat_state().get_next())


class BeatState:


    def __init__(self, game_state: 'GameState'):
        self.game_state = game_state
        
        
    def process(self):
        pass
        
        
    def get_next(self) -> 'BeatState':
        return self._get_next_state_class()(self.game_state)
        
        
    def _get_next_state_class(self) -> type:
        raise NotImplementedError()
        
        
class SetPairs(BeatState):
    def _get_next_state_class(self) -> type:
        return SetAntes
    
    
class SetAntes(BeatState):
    def _get_next_state_class(self) -> type:
        return Reveal
    
    
class Reveal(BeatState):
    def _get_next_state_class(self) -> type:
        return CheckForClash
    
    
class CheckForClash(BeatState):
    def _get_next_state_class(self) -> type:
        return StartOfBeat
    
    
class StartOfBeat(BeatState):
    def _get_next_state_class(self) -> type:
        return ActiveBefore
    
    
class ActiveBefore(BeatState):
    def _get_next_state_class(self) -> type:
        return ActiveCheckRange
            
    
class ActiveCheckRange(BeatState):
    pass