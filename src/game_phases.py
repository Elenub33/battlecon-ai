from .agent import Agent
from .game_state import GameState
from .fighters.fighter import FighterState

class PhaseStateMachine:

    set: 'Set'
    ante: 'Ante'
    reveal: 'Reveal'
    clash: 'Clash'
    start_of_beat: 'StartOfBeat'
    active_before: 'ActiveBefore'
    active_check_range: 'ActiveCheckRange'
    active_hit: 'ActiveHit'
    active_damage: 'ActiveDamage'
    active_after: 'ActiveAfter'
    reactive_before: 'ReactiveBefore'
    reactive_check_range: 'ReactiveCheckRange'
    reactive_hit: 'ReactiveHit'
    reactive_damage: 'ReactiveDamage'
    reactive_after: 'ReactiveAfter'
    end_of_beat: 'EndOfBeat'
    recycle: 'Recycle'
    state: 'PhaseState'

    def __init__(self):
        self.set = Set()
        self.ante = Ante()
        self.reveal = Reveal()
        self.clash = Clash()
        self.start_of_beat = StartOfBeat()
        self.active_before = ActiveBefore()
        self.active_check_range = ActiveCheckRange()
        self.active_hit = ActiveHit()
        self.active_damage = ActiveDamage()
        self.active_after = ActiveAfter()
        self.reactive_before = ReactiveBefore()
        self.reactive_check_range = ReactiveCheckRange()
        self.reactive_hit = ReactiveHit()
        self.reactive_damage = ReactiveDamage()
        self.reactive_after = ReactiveAfter()
        self.end_of_beat = EndOfBeat()
        self.recycle = Recycle()

        self.set_state(self.set)
        

    def do_next(self, game_state: GameState, agents: list[Agent]) -> None:
        self.state.do(game_state, agents)
        self.set_state(self.state.next_state(self, game_state))


    def set_state(self, phase_state: 'PhaseState') -> None:
        self.state = phase_state


class PhaseState:
    def do(self, game_state: GameState, agents: list[Agent]):
        raise NotImplementedError()
    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> 'PhaseState':
        raise NotImplementedError()


# -------------------------------------------------
# parent classes for all attack-based engine states
# -------------------------------------------------
class AttackState(PhaseState):
    def get_attacking_fighter_state(self, game_state: GameState) -> FighterState:
        raise NotImplementedError()
    def get_defending_fighter_state(self, game_state: GameState):
        raise NotImplementedError()
        
        
class ActiveAttackState(AttackState):
    def get_attacking_fighter_state(self, game_state: GameState):
        return game_state.get_active_fighter_state()
    def get_defending_fighter_state(self, game_state: GameState):
        return game_state.get_reactive_fighter_state()
        
        
class ReactiveAttackState(AttackState):
    def get_attacking_fighter_state(self, game_state: GameState):
        return game_state.get_reactive_fighter_state()
    def get_defending_fighter_state(self, game_state: GameState):
        return game_state.get_active_fighter_state()


# ------------------------------------------------------ 
# parent classes for specific attack-based engine states
# ------------------------------------------------------
class CheckRangeState(AttackState):
    def opponent_in_range(self, game_state: GameState) -> bool:
        range = self.get_attacking_fighter_state(game_state).get_attack_strategy().get_range()
        distance = state.get_distance_between_fighters()
        return range[0] >= distance and range[1] <= distance
# ------------------------------------------------------


class Set(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.ante


class Ante(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.reveal
        


class Reveal(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        # TODO: check for clash
        return state_machine.start_of_beat


class Clash(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        # TODO: skip beat if out of cards from clashing
        return state_machine.start_of_beat
    
    
class StartOfBeat(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.active_before


class ActiveBefore(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.active_check_range


class ActiveCheckRange(ActiveAttackState, CheckRangeState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        if self.opponent_in_range(game_state):
            return state_machine.active_hit
        else:
            return state_machine.active_after
            
    
class ActiveHit(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.active_damage
            
    
class ActiveDamage(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.active_after
            
    
class ActiveAfter(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        if self.get_game_state().get_reactive_fighter_state().is_stunned():
            return state_machine.end_of_beat
        else:
            return state_machine.reactive_before
            

class ReactiveBefore(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.reactive_check_range


class ReactiveCheckRange(ActiveAttackState, CheckRangeState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        if self.opponent_in_range(game_state):
            return state_machine.reactive_hit
        else:
            return state_machine.reactive_after
            
    
class ReactiveHit(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.reactive_damage
            
    
class ReactiveDamage(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.reactive_after
            
    
class ReactiveAfter(ActiveAttackState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.end_of_beat
            
    
class EndOfBeat(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        pass

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.recycle
            
    
class Recycle(PhaseState):

    def do(self, game_state: GameState, agents: list[Agent]):
        # TODO: remove this
        programPause = raw_input("Beat complete.\nPress the <ENTER> key to continue...")

    def next_state(self, state_machine: PhaseStateMachine, game_state: GameState) -> PhaseState:
        return state_machine.set