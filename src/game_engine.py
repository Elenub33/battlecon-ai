import random
import game_state, agent, fighter
    

class GameEngine:


    def __init__(self, agent0, agent1):
        assert isinstance(agent0, agent.Agent)
        assert isinstance(agent1, agent.Agent)
        self.agents = [agent0, agent1]
        self.engine_state = None
    
    
    def initialize_from_start(self):
        self.engine_state = EngineState.from_start(self)
    
    
    def initialize_from_file(self):
        raise NotImplementedError()
    
    
    def get_active_agent(self) -> agent.Agent:
        active_fighter = self.get_game_state().get_active_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find active agent.")
    
    
    def get_reactive_agent(self) -> agent.Agent:
        active_fighter = self.get_game_state().get_reactive_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find reactive agent.")
        
        
    def get_engine_state(self) -> 'EngineState':
        return self.engine_state
        
    
    def set_engine_state(self, state: 'EngineState'):
        self.engine_state = state
        
        
    def get_game_state(self) -> game_state.GameState:
        return self.get_engine_state().get_game_state()
        
        
    def process(self):
        self.get_engine_state().handle()
        self.advance_engine_state()
    
    
    def advance_engine_state(self):    
        self.set_engine_state(self.get_engine_state().get_next())
        

class EngineState:


    @staticmethod
    def from_start(engine: GameEngine):
        state = game_state.GameState(engine.agents[0].get_fighter(), engine.agents[1].get_fighter())
        state.initialize_from_start()
        return SetPairs(engine, state)


    def __init__(self, engine: GameEngine, state: game_state.GameState):
        self.engine = engine
        self.game_state = state
        
        
    def get_engine(self) -> GameEngine:
        return self.engine
        
        
    def get_game_state(self):
        return self.game_state
        
        
    def handle(self):
        pass
        
        
    def get_next(self) -> 'EngineState':
        return self.get_next_state_class()(self.get_engine(), self.get_game_state())
        
        
    def get_next_state_class(self) -> type:
        raise NotImplementedError()
        
        
class SetPairs(EngineState):
    def get_next_state_class(self) -> type:
        return SetAntes
    
    
class SetAntes(EngineState):
    def get_next_state_class(self) -> type:
        return Reveal
    
    
class Reveal(EngineState):
    def get_next_state_class(self) -> type:
        return CheckForClash
    
    
class CheckForClash(EngineState):
    def get_next_state_class(self) -> type:
        return StartOfBeat
    
    
class StartOfBeat(EngineState):
    def get_next_state_class(self) -> type:
        return ActiveBefore
    
    
# -------------------------------------------------
# parent classes for all attack-based engine states
# -------------------------------------------------
class AttackState(EngineState):
    def get_attacking_fighter_state(self) -> fighter.Fighter:
        raise NotImplementedError()
        
        
class ActiveAttackState(AttackState):
    def get_attacking_fighter_state(self) -> fighter.Fighter:
        return self.get_game_state().get_active_fighter_state()
    def get_defending_fighter_state(self) -> fighter.Fighter:
        return self.get_game_state().get_reactive_fighter_state()
        
        
class ReactiveAttackState(AttackState):
    def get_attacking_fighter_state(self) -> fighter.Fighter:
        return self.get_game_state().get_reactive_fighter_state()
    def get_defending_fighter_state(self) -> fighter.Fighter:
        return self.get_game_state().get_active_fighter_state()
        
        
# ------------------------------------------------------
# parent classes for specific attack-based engine states
# ------------------------------------------------------
class CheckRangeState(AttackState):
    def opponent_in_range(self) -> bool:
        range = self.get_attacking_fighter_state().get_attack_strategy().get_range()
        distance = self.get_game_state().get_distance_between_fighters()
        return range[0] >= distance and range[1] <= distance
# ------------------------------------------------------

    
class ActiveBefore(EngineState):
    def get_next_state_class(self) -> type:
        return ActiveCheckRange
            
    
class ActiveCheckRange(ActiveAttackState, CheckRangeState):
    def get_next_state_class(self) -> type:
        if self.opponent_in_range():
            return ActiveHit
        else:
            return ActiveAfter
            
    
class ActiveHit(EngineState):
    def get_next_state_class(self) -> type:
        return ActiveDamage
            
    
class ActiveDamage(EngineState):
    def get_next_state_class(self) -> type:
        return ActiveAfter
            
    
class ActiveAfter(EngineState):
    def get_next_state_class(self) -> type:
        if self.get_game_state().get_reactive_fighter_state().is_stunned():
            return EndOfBeat
        else:
            return ReactiveBefore
            
    
class ReactiveBefore(EngineState):
    def get_next_state_class(self) -> type:
        return ReactiveCheckRange
            
    
class ReactiveCheckRange(ReactiveAttackState, CheckRangeState):
    def get_next_state_class(self) -> type:
        if self.opponent_in_range():
            return ReactiveHit
        else:
            return ReactiveAfter
            
    
class ReactiveHit(EngineState):
    def get_next_state_class(self) -> type:
        return ReactiveDamage
            
    
class ReactiveDamage(EngineState):
    def get_next_state_class(self) -> type:
        return ReactiveAfter
            
    
class ReactiveAfter(EngineState):
    def get_next_state_class(self) -> type:
        return EndOfBeat
            
    
class EndOfBeat(EngineState):
    def get_next_state_class(self) -> type:
        return Recycle
            
    
class Recycle(EngineState):
    def get_next_state_class(self) -> type:
        return SetPairs