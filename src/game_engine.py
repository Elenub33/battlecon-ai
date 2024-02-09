import random
from .agent import Agent
from .game_state import GameState


class GameEngine:


    def __init__(self, agent0, agent1):
        assert isinstance(agent0, Agent)
        assert isinstance(agent1, Agent)
        self.agents = [agent0, agent1]
        self.set_game_state(None)
        self.set_phase_state(None)
    
    
    def initialize_from_start(self):
        self.set_game_state(GameState.from_start(self.agents[0].get_fighter(), self.agents[1].get_fighter()))
        self.set_phase_state(PhaseState.from_start(self))
    
    
    def initialize_from_file(self):
        raise NotImplementedError()
    
    
    def get_active_agent(self) -> Agent:
        active_fighter = self.get_game_state().get_active_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find active agent.")
    
    
    def get_reactive_agent(self) -> Agent:
        active_fighter = self.get_game_state().get_reactive_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find reactive agent.")
        

    # resolve_phase resolves the current phase and advances to the next.
    def resolve_phase(self):
        print("Resolving phase", self.get_phase_state().__class__)
        self.get_phase_state().resolve()
        self.advance_phase_state()
        input("Press enter to continue.")

        
    def get_phase_state(self) -> 'PhaseState':
        return self.phase_state
        
    
    def set_phase_state(self, state: 'PhaseState'):
        self.phase_state = state
        
        
    def get_game_state(self) -> GameState:
        return self.game_state
        
        
    def set_game_state(self, new_game_state: GameState):
        self.game_state = new_game_state
        
        
    def process(self):
        self.get_phase_state().handle()
        self.advance_phase_state()
    
    
    def advance_phase_state(self):    
        self.set_phase_state(self.get_phase_state().get_next_phase())
        

class PhaseState:


    @staticmethod
    def from_start(engine: GameEngine):
        return SetPairs(engine)


    def __init__(self, engine: GameEngine):
        self._engine = engine
        
        
    def get_engine(self) -> GameEngine:
        return self._engine
        
        
    def get_game_state(self):
        return self.get_engine().get_game_state()
        
        
    def resolve(self):
        pass
        
        
    def get_next_phase(self) -> 'PhaseState':
        return self.get_next_state_class()(self.get_engine())
        
        
    def get_next_state_class(self) -> type:
        raise NotImplementedError()
        
        
class SetPairs(PhaseState):
    def get_next_state_class(self) -> type:
        return SetAntes
    def resolve(self):
        eng = self.get_engine()
        eng.get_active_agent().choose_attack_pair() # TODO: define decisions, etc.
    
    
class SetAntes(PhaseState):
    def get_next_state_class(self) -> type:
        return Reveal
    
    
class Reveal(PhaseState):
    def get_next_state_class(self) -> type:
        return CheckForClash
    
    
class CheckForClash(PhaseState):
    def get_next_state_class(self) -> type:
        return StartOfBeat
    
    
class StartOfBeat(PhaseState):
    def get_next_state_class(self) -> type:
        return ActiveBefore
    
    
# -------------------------------------------------
# parent classes for all attack-based engine states
# -------------------------------------------------
class AttackState(PhaseState):
    def get_attacking_fighter_state(self):
        raise NotImplementedError()
    def get_defending_fighter_state(self):
        raise NotImplementedError()
        
        
class ActiveAttackState(AttackState):
    def get_attacking_fighter_state(self):
        return self.get_game_state().get_active_fighter_state()
    def get_defending_fighter_state(self):
        return self.get_game_state().get_reactive_fighter_state()
        
        
class ReactiveAttackState(AttackState):
    def get_attacking_fighter_state(self):
        return self.get_game_state().get_reactive_fighter_state()
    def get_defending_fighter_state(self):
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

    
class ActiveBefore(PhaseState):
    def get_next_state_class(self) -> type:
        return ActiveCheckRange
            
    
class ActiveCheckRange(ActiveAttackState, CheckRangeState):
    def get_next_state_class(self) -> type:
        if self.opponent_in_range():
            return ActiveHit
        else:
            return ActiveAfter
            
    
class ActiveHit(PhaseState):
    def get_next_state_class(self) -> type:
        return ActiveDamage
            
    
class ActiveDamage(PhaseState):
    def get_next_state_class(self) -> type:
        return ActiveAfter
            
    
class ActiveAfter(PhaseState):
    def get_next_state_class(self) -> type:
        if self.get_game_state().get_reactive_fighter_state().is_stunned():
            return EndOfBeat
        else:
            return ReactiveBefore
            
    
class ReactiveBefore(PhaseState):
    def get_next_state_class(self) -> type:
        return ReactiveCheckRange
            
    
class ReactiveCheckRange(ReactiveAttackState, CheckRangeState):
    def get_next_state_class(self) -> type:
        if self.opponent_in_range():
            return ReactiveHit
        else:
            return ReactiveAfter
            
    
class ReactiveHit(PhaseState):
    def get_next_state_class(self) -> type:
        return ReactiveDamage
            
    
class ReactiveDamage(PhaseState):
    def get_next_state_class(self) -> type:
        return ReactiveAfter
            
    
class ReactiveAfter(PhaseState):
    def get_next_state_class(self) -> type:
        return EndOfBeat
            
    
class EndOfBeat(PhaseState):
    def get_next_state_class(self) -> type:
        return Recycle
            
    
class Recycle(PhaseState):
    def get_next_state_class(self) -> type:
        return SetPairs