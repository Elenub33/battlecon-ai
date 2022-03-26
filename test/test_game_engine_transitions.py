import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import game_engine, agent, fighter, strategy, game_element


class TestGameEngineTransitions(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.f0 = fighter.Fighter()
        self.f1 = fighter.Fighter()
        self.agt0 = agent.Agent(self.f0)
        self.agt1 = agent.Agent(self.f1)
        self.game = game_engine.GameEngine(self.agt0, self.agt1)
        self.game.initialize_from_start()
        self.game_state = self.game.get_game_state()
        
        
    def _test_beat_state_advance(self, end_state_cls):
        self.game.advance_engine_state()
        engine_state = self.game.get_engine_state()
        self.assertTrue(isinstance(engine_state, end_state_cls), "Transitioned to {} instead of instance of {}.".format(engine_state, end_state_cls))
        
        
    def test_set_pairs_leads_to_set_antes(self):
        self.game.set_engine_state(game_engine.SetPairs(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.SetAntes)
        
        
    def test_set_antes_leads_to_reveal(self):
        self.game.set_engine_state(game_engine.SetAntes(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.Reveal)
        
        
    def test_reveal_leads_to_check_for_clash(self):
        self.game.set_engine_state(game_engine.Reveal(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.CheckForClash)
        
        
    def test_check_for_clash_leads_to_start_of_beat(self):
        self.game.set_engine_state(game_engine.CheckForClash(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.StartOfBeat)
        
        
    def test_start_of_beat_leads_to_active_before(self):
        self.game.set_engine_state(game_engine.StartOfBeat(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.ActiveBefore)
        
        
    def test_active_before_leads_to_active_check_range(self):
        self.game.set_engine_state(game_engine.ActiveBefore(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.ActiveCheckRange)
        
        
    def test_active_check_range_leads_to_active_hit_if_in_range(self):
        
        self.game.get_game_state().set_fighter_position(self.f0, 2)
        self.game.get_game_state().set_fighter_position(self.f1, 4)
        
        elt = game_element.GameElement()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = strategy.AttackStrategy(elt)
        
        self.game.get_game_state().get_fighter_state(self.f0).set_attack_strategy(strat)
        self.game.get_game_state().get_fighter_state(self.f1).set_attack_strategy(strat)
        
        self.game.set_engine_state(game_engine.ActiveCheckRange(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.ActiveHit)
        
        
    def test_active_check_range_leads_to_active_after_if_not_in_range(self):
        
        self.game.get_game_state().set_fighter_position(self.f0, 2)
        self.game.get_game_state().set_fighter_position(self.f1, 5)
        
        elt = game_element.GameElement()
        elt.set_min_range(2)
        elt.set_max_range(2)
        strat = strategy.AttackStrategy(elt)
        
        self.game.get_game_state().get_fighter_state(self.f0).set_attack_strategy(strat)
        self.game.get_game_state().get_fighter_state(self.f1).set_attack_strategy(strat)
        
        self.game.set_engine_state(game_engine.ActiveCheckRange(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.ActiveAfter)
        
        self.game.get_game_state().set_fighter_position(self.f1, 3)
        
        self.game.set_engine_state(game_engine.ActiveCheckRange(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.ActiveAfter)
        
        
    def test_active_hit_leads_to_active_damage(self):
        self.game.set_engine_state(game_engine.ActiveHit(self.game, self.game.get_game_state()))
        self._test_beat_state_advance(game_engine.ActiveDamage)
        

if __name__ == "__main__":
    unittest.main()
