import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
from agent_random import RandomAgent

class TestGame(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.agt0 = RandomAgent("")
        self.agt1 = RandomAgent("")
        self.game = battlecon.Game(self.agt0, self.agt1)
        
        
    @unittest.skip("Incomplete test.")
    def test_execute_beat(self):
        self.game.execute_beat() # TODO: test the functionality of execute_beat
        
        
    def test_initial_active_and_inactive(self):
        self.game.initialize_from_start()
        self.assertTrue(
            (self.game.get_active_player() == self.agt0 and self.game.get_reactive_player() == self.agt1) or
            (self.game.get_active_player() == self.agt1 and self.game.get_reactive_player() == self.agt0),
            "Active and reactive players were not initialized correctly."
        )
        
    
    def test_error_if_non_agent_passed_into_constructor(self):
        with self.assertRaises(AssertionError) as context:
            battlecon.Game(self.agt0, 6)
        with self.assertRaises(AssertionError) as context:
            battlecon.Game(6, self.agt1)
        
        
    def test_get_state(self):
        state = self.game.get_state()
        self.assertTrue(isinstance(state, battlecon.GameState), "State returned by get_state was not a GameState object.")
        

if __name__ == "__main__":
    unittest.main()
