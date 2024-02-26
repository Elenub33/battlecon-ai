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

    def do_next(self, game_state: GameState) -> None:
        self.state.do(game_state)
        self.state.next(self, game_state)

    def set_state(self, phase_state: 'PhaseState') -> None:
        self.state = phase_state


class PhaseState:

    def do(self, game_state: GameState):
        raise NotImplementedError()
    
    def next(self, state_machine: PhaseStateMachine, game_state: GameState):
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
    def opponent_in_range(self) -> bool:
        range = self.get_attacking_fighter_state().get_attack_strategy().get_range()
        distance = self.get_game_state().get_distance_between_fighters()
        return range[0] >= distance and range[1] <= distance
# ------------------------------------------------------


class Set(PhaseState):

    def do(self, game_state: GameState):
        pass

    def next(self, state_machine: PhaseStateMachine, game_state: GameState):
        state_machine.set_state(state_machine.ante)


class Ante(PhaseState):

    def do(self, game_state: GameState):
        pass

    def next(self, state_machine: PhaseStateMachine, game_state: GameState):
        state_machine.set_state(state_machine.reveal)


class Reveal(PhaseState):

    def do(self, game_state: GameState):
        pass

    def next(self, state_machine: PhaseStateMachine, game_state: GameState):
        # TODO: check for clash
        state_machine.set_state(state_machine.start_of_beat)


class Clash(PhaseState):

    def do(self, game_state: GameState):
        pass

    def next(self, state_machine: PhaseStateMachine, game_state: GameState):
        state_machine.set_state(state_machine.start_of_beat)
    
    
class StartOfBeat(PhaseState):
    pass

    
class ActiveBefore(PhaseState):
    pass


class ActiveCheckRange(ActiveAttackState, CheckRangeState):
    def get_next_state_class(self) -> type:
        if self.opponent_in_range():
            return ActiveHit
        else:
            return ActiveAfter
            
    
class ActiveHit(PhaseState):
    pass
            
    
class ActiveDamage(PhaseState):
    pass
            
    
class ActiveAfter(PhaseState):
    def get_next_state_class(self) -> type:
        if self.get_game_state().get_reactive_fighter_state().is_stunned():
            return EndOfBeat
        else:
            return ReactiveBefore
            
    
class ReactiveBefore(PhaseState):
    pass
            
    
class ReactiveCheckRange(ReactiveAttackState, CheckRangeState):
    def get_next_state_class(self) -> type:
        if self.opponent_in_range():
            return ReactiveHit
        else:
            return ReactiveAfter
            
    
class ReactiveHit(PhaseState):
    pass
            
    
class ReactiveDamage(PhaseState):
    pass
            
    
class ReactiveAfter(PhaseState):
    pass
            
    
class EndOfBeat(PhaseState):
    pass
            
    
class Recycle(PhaseState):
    pass