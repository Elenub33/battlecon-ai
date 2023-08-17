import unittest

from src.fighters.fighter import Fighter
from src import game_engine
from src.agent import Agent
from src.strategy import AttackStrategy
from src.fighters.elements.element import Element


class TestGameEngineTransitions(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.f0 = Fighter()
        self.f1 = Fighter()
        self.agt0 = Agent(self.f0)
        self.agt1 = Agent(self.f1)
        self.game = game_engine.GameEngine(self.agt0, self.agt1)
        self.game.initialize_from_start()
        self.game_state = self.game.get_game_state()
        
        
    def _test_beat_state_advance(self, start_state_cls, end_state_cls):
        self.game.set_phase_state(start_state_cls(self.game))
        self.game.advance_phase_state()
        phase_state = self.game.get_phase_state()
        self.assertTrue(isinstance(phase_state, end_state_cls), "Transitioned from {} to {} instead of instance of {}.".format(start_state_cls, phase_state, end_state_cls))
        
        
    def test_set_pairs_leads_to_set_antes(self):
        self._test_beat_state_advance(game_engine.SetPairs, game_engine.SetAntes)
        
        
    def test_set_antes_leads_to_reveal(self):
        self._test_beat_state_advance(game_engine.SetAntes, game_engine.Reveal)
        
        
    def test_reveal_leads_to_check_for_clash(self):
        self._test_beat_state_advance(game_engine.Reveal, game_engine.CheckForClash)
        
        
    def test_check_for_clash_leads_to_start_of_beat(self):
        self._test_beat_state_advance(game_engine.CheckForClash, game_engine.StartOfBeat)
        
        
    def test_start_of_beat_leads_to_active_before(self):
        self._test_beat_state_advance(game_engine.StartOfBeat, game_engine.ActiveBefore)
        
        
    def test_active_before_leads_to_active_check_range(self):
        self._test_beat_state_advance(game_engine.ActiveBefore, game_engine.ActiveCheckRange)
        
        
    def test_active_check_range_leads_to_active_hit_if_in_range(self):
        
        self.game_state.clear_fighter_positions()
        self.game.get_game_state().set_fighter_position(self.f0, 2)
        self.game.get_game_state().set_fighter_position(self.f1, 4)
        
        elt = Element()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = AttackStrategy(elt)
        
        self.game.get_game_state().get_fighter_state(self.game.get_game_state().get_active_fighter()).set_attack_strategy(strat)
        
        self._test_beat_state_advance(game_engine.ActiveCheckRange, game_engine.ActiveHit)
        
        
    def test_active_check_range_leads_to_active_after_if_not_in_range(self):
        
        self.game_state.clear_fighter_positions()
        self.game.get_game_state().set_fighter_position(self.f0, 2)
        self.game.get_game_state().set_fighter_position(self.f1, 5)
        
        elt = Element()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = AttackStrategy(elt)
        
        self.game.get_game_state().get_fighter_state(self.game.get_game_state().get_active_fighter()).set_attack_strategy(strat)
        
        self._test_beat_state_advance(game_engine.ActiveCheckRange, game_engine.ActiveAfter)
        
        self.game.get_game_state().set_fighter_position(self.f1, 3)
        
        self._test_beat_state_advance(game_engine.ActiveCheckRange, game_engine.ActiveAfter)
        
        
    def test_active_hit_leads_to_active_damage(self):
        self._test_beat_state_advance(game_engine.ActiveHit, game_engine.ActiveDamage)
        
        
    def test_active_damage_leads_to_active_after(self):
        self._test_beat_state_advance(game_engine.ActiveDamage, game_engine.ActiveAfter)
        
        
    def test_active_after_leads_to_reactive_before_if_reactive_not_stunned(self):
        self.game.get_game_state().get_fighter_state(self.game.get_game_state().get_reactive_fighter()).set_stunned(False)
        self._test_beat_state_advance(game_engine.ActiveAfter, game_engine.ReactiveBefore)
        
        
    def test_active_after_leads_to_end_of_beat_if_reactive_stunned(self):
        self.game.get_game_state().get_fighter_state(self.game.get_game_state().get_reactive_fighter()).set_stunned(True)
        self._test_beat_state_advance(game_engine.ActiveAfter, game_engine.EndOfBeat)
        
        
    def test_reactive_before_leads_to_reactive_check_range(self):
        self._test_beat_state_advance(game_engine.ReactiveBefore, game_engine.ReactiveCheckRange)
        
        
    def test_reactive_check_range_leads_to_reactive_hit_if_in_range(self):
        
        self.game_state.clear_fighter_positions()
        self.game.get_game_state().set_fighter_position(self.f0, 2)
        self.game.get_game_state().set_fighter_position(self.f1, 4)
        
        elt = Element()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = AttackStrategy(elt)
        
        self.game.get_game_state().get_fighter_state(self.game.get_game_state().get_reactive_fighter()).set_attack_strategy(strat)
        
        self._test_beat_state_advance(game_engine.ReactiveCheckRange, game_engine.ReactiveHit)
        
        
    def test_reactive_check_range_leads_to_reactive_after_if_not_in_range(self):
        
        self.game_state.clear_fighter_positions()
        self.game.get_game_state().set_fighter_position(self.f0, 2)
        self.game.get_game_state().set_fighter_position(self.f1, 5)
        
        elt = Element()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = AttackStrategy(elt)
        
        self.game.get_game_state().get_fighter_state(self.game.get_game_state().get_reactive_fighter()).set_attack_strategy(strat)
        
        self._test_beat_state_advance(game_engine.ReactiveCheckRange, game_engine.ReactiveAfter)
        
        self.game.get_game_state().set_fighter_position(self.f1, 3)
        
        self._test_beat_state_advance(game_engine.ReactiveCheckRange, game_engine.ReactiveAfter)
        
        
    def test_reactive_hit_leads_to_reactive_damage(self):
        self._test_beat_state_advance(game_engine.ReactiveHit, game_engine.ReactiveDamage)
        
        
    def test_reactive_damage_leads_to_reactive_after(self):
        self._test_beat_state_advance(game_engine.ReactiveDamage, game_engine.ReactiveAfter)
        
        
    def test_reactive_after_leads_to_end_of_beat(self):
        self._test_beat_state_advance(game_engine.ReactiveAfter, game_engine.EndOfBeat)
        
        
    def test_end_of_beat_leads_to_recycle(self):
        self._test_beat_state_advance(game_engine.EndOfBeat, game_engine.Recycle)
        
        
    def test_recycle_leads_to_set_pairs(self):
        self._test_beat_state_advance(game_engine.Recycle, game_engine.SetPairs)
        

if __name__ == "__main__":
    unittest.main()
