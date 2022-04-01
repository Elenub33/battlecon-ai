import unittest
import src.game_engine as game_engine, src.game_state as game_state, src.fighters.fighter as fighter, src.agent as agent

class TestGameEngine(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.agt0 = agent.Agent(fighter.Fighter())
        self.agt1 = agent.Agent(fighter.Fighter())
        self.game = game_engine.GameEngine(self.agt0, self.agt1)
        
        
    def test_initial_active_and_inactive(self):
        self.game.initialize_from_start()
        self.assertTrue(
            (self.game.get_active_agent() == self.agt0 and self.game.get_reactive_agent() == self.agt1) or
            (self.game.get_active_agent() == self.agt1 and self.game.get_reactive_agent() == self.agt0),
            "Active and reactive players were not initialized correctly."
        )
        
    
    def test_error_if_non_agent_passed_into_constructor(self):
        with self.assertRaises(AssertionError) as context:
            game_engine.GameEngine(self.agt0, 6)
        with self.assertRaises(AssertionError) as context:
            game_engine.GameEngine(6, self.agt1)
        
        
    def test_get_game_state(self):
        self.game.initialize_from_start()
        state = self.game.get_game_state()
        self.assertTrue(isinstance(state, game_state.GameState), "State returned by get_state was not a GameState object.")
        self.assertTrue(self.agt0.get_fighter() == state.get_active_fighter() or self.agt0.get_fighter() == state.get_reactive_fighter(), "Returned state did not contain agent 0's fighter.")
        self.assertTrue(self.agt1.get_fighter() == state.get_active_fighter() or self.agt1.get_fighter() == state.get_reactive_fighter(), "Returned state did not contain agent 1's fighter.")
        
        
    def test_initial_fighter_positions(self):
        self.game.initialize_from_start()
        state = self.game.get_game_state()
        positions = set()
        positions.add(state.get_active_fighter_state().get_position())
        positions.add(state.get_reactive_fighter_state().get_position())
        self.assertEqual(positions, set([2, 4]), "Expected fighter positions to start at 2 and 4.")
        

if __name__ == "__main__":
    unittest.main()
