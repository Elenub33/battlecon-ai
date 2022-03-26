import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon, fighter, agent, strategy

class TestGame(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.agt0 = agent.Agent(fighter.Fighter())
        self.agt1 = agent.Agent(fighter.Fighter())
        self.game = battlecon.Game(self.agt0, self.agt1)
        
        
    @unittest.skip("Incomplete test.")
    def test_execute_beat(self):
        self.game.execute_beat() # TODO: test the functionality of execute_beat
        
        
    def test_initial_active_and_inactive(self):
        self.game.initialize_from_start()
        self.assertTrue(
            (self.game.get_active_agent() == self.agt0 and self.game.get_reactive_agent() == self.agt1) or
            (self.game.get_active_agent() == self.agt1 and self.game.get_reactive_agent() == self.agt0),
            "Active and reactive players were not initialized correctly."
        )
        
        
    def test_initial_active_player_is_random(self):
        agt0_active = False
        agt1_active = False
        for i in range(0, 100):
            self.game.initialize_from_start()
            if self.game.get_active_agent() == self.agt0:
                agt0_active = True
            elif self.game.get_active_agent() == self.agt1:
                agt1_active = True
            if agt0_active and agt1_active:
                break
        self.assertTrue(agt0_active, "Agent 0 was never the active player in 100 attempts.")
        self.assertTrue(agt1_active, "Agent 1 was never the active player in 100 attempts.")
    
    
    def test_error_if_non_agent_passed_into_constructor(self):
        with self.assertRaises(AssertionError) as context:
            battlecon.Game(self.agt0, 6)
        with self.assertRaises(AssertionError) as context:
            battlecon.Game(6, self.agt1)
        
        
    def test_get_state(self):
        state = self.game.get_state()
        self.assertTrue(isinstance(state, battlecon.GameState), "State returned by get_state was not a GameState object.")
        self.assertTrue(self.agt0.get_fighter() == state.get_active_fighter() or self.agt0.get_fighter() == state.get_reactive_fighter(), "Returned state did not contain agent 0's fighter.")
        self.assertTrue(self.agt1.get_fighter() == state.get_active_fighter() or self.agt1.get_fighter() == state.get_reactive_fighter(), "Returned state did not contain agent 1's fighter.")
        
        
    def test_get_attack_strategy(self):
        strat0 = strategy.AttackStrategy()
        strat1 = strategy.AttackStrategy()
        self.game.get_state().set_fighter_strategy(self.agt0.get_fighter(), strat0)
        self.assertEqual(self.game.get_state().get_fighter_state(self.agt0.get_fighter()).get_attack_strategy(), strat0)
        self.game.get_state().set_fighter_strategy(self.agt1.get_fighter(), strat1)
        self.assertEqual(self.game.get_state().get_fighter_state(self.agt1.get_fighter()).get_attack_strategy(), strat1)
        

if __name__ == "__main__":
    unittest.main()
