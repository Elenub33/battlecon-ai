import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon, agent, fighter, strategy, game_element

class TestBeatTransitions(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.f0 = fighter.Fighter()
        self.f1 = fighter.Fighter()
        self.game_state = battlecon.GameState(self.f0, self.f1)
        
        
    def _test_beat_state_advance(self, end_state_cls):
        self.game_state.advance_beat_state()
        beat_state = self.game_state.get_beat_state()
        self.assertTrue(isinstance(beat_state, end_state_cls), "Transitioned to {} instead of instance of {}.".format(beat_state, end_state_cls))
        
        
    def test_set_pairs_leads_to_set_antes(self):
        self.game_state.set_beat_state(battlecon.SetPairs(self.game_state))
        self._test_beat_state_advance(battlecon.SetAntes)
        
        
    def test_set_antes_leads_to_reveal(self):
        self.game_state.set_beat_state(battlecon.SetAntes(self.game_state))
        self._test_beat_state_advance(battlecon.Reveal)
        
        
    def test_reveal_leads_to_check_for_clash(self):
        self.game_state.set_beat_state(battlecon.Reveal(self.game_state))
        self._test_beat_state_advance(battlecon.CheckForClash)
        
        
    def test_check_for_clash_leads_to_start_of_beat(self):
        self.game_state.set_beat_state(battlecon.CheckForClash(self.game_state))
        self._test_beat_state_advance(battlecon.StartOfBeat)
        
        
    def test_start_of_beat_leads_to_active_before(self):
        self.game_state.set_beat_state(battlecon.StartOfBeat(self.game_state))
        self._test_beat_state_advance(battlecon.ActiveBefore)
        
        
    def test_active_before_leads_to_active_check_range(self):
        self.game_state.set_beat_state(battlecon.ActiveBefore(self.game_state))
        self._test_beat_state_advance(battlecon.ActiveCheckRange)
        
        
    def test_active_check_range_leads_to_active_hit_if_in_range(self):
        
        self.game_state.set_fighter_position(self.f0, 2)
        self.game_state.set_fighter_position(self.f1, 4)
        
        elt = game_element.GameElement()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = strategy.AttackStrategy(elt)
        
        self.game_state.set_fighter_strategy(self.f0, strat)
        self.game_state.set_fighter_strategy(self.f1, strat)
        
        self.game_state.set_beat_state(battlecon.ActiveCheckRange(self.game_state))
        self._test_beat_state_advance(battlecon.ActiveHit)
        
        
    def test_active_check_range_leads_to_active_after_if_not_in_range(self):
        
        self.game_state.set_fighter_position(self.f0, 2)
        self.game_state.set_fighter_position(self.f1, 5)
        
        elt = game_element.GameElement()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = strategy.AttackStrategy(elt)
        
        self.game_state.set_fighter_strategy(self.f0, strat)
        self.game_state.set_fighter_strategy(self.f1, strat)
        
        self.game_state.set_beat_state(battlecon.ActiveCheckRange(self.game_state))
        self._test_beat_state_advance(battlecon.ActiveAfter)
        
        self.game_state.set_fighter_position(self.f1, 3)
        
        self.game_state.set_beat_state(battlecon.ActiveCheckRange(self.game_state))
        self._test_beat_state_advance(battlecon.ActiveAfter)
        
        
    def test_active_hit_leads_to_active_damage(self):
        self.game_state.set_beat_state(battlecon.ActiveHit(self.game_state))
        self._test_beat_state_advance(battlecon.ActiveDamage)
        

if __name__ == "__main__":
    unittest.main()
