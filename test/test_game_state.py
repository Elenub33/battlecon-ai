import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import game_state, fighter

class TestGameState(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.f0 = fighter.Fighter()
        self.f1 = fighter.Fighter()
        self.state = game_state.GameState(self.f0, self.f1)
        
        
    def test_initial_active_and_inactive(self):
        self.state.initialize_from_start()
        self.assertTrue(
            (self.state.get_active_fighter() == self.f0 and self.state.get_reactive_fighter() == self.f1) or
            (self.state.get_active_fighter() == self.f1 and self.state.get_reactive_fighter() == self.f0),
            "Active and reactive players were not initialized correctly."
        )
        
        
    def test_initial_active_fighter_is_random(self):
        f0_active = False
        f1_active = False
        for i in range(0, 100):
            self.state.initialize_from_start()
            if self.state.get_active_fighter() == self.f0:
                f0_active = True
            elif self.state.get_active_fighter() == self.f1:
                f1_active = True
            if f0_active and f1_active:
                break
        self.assertTrue(f0_active, "Fighter 0 was never the active fighter in 100 attempts.")
        self.assertTrue(f1_active, "Fighter 1 was never the active fighter in 100 attempts.")
        
        
    def test_get_distance_between_fighters(self):
    
        self.state.initialize_from_start()
        self.state.clear_fighter_positions()
        
        self.state.set_fighter_position(self.f0, 2)
        self.state.set_fighter_position(self.f1, 3)
        self.assertEqual(self.state.get_distance_between_fighters(), 1)
        
        self.state.set_fighter_position(self.f0, 0)
        self.state.set_fighter_position(self.f1, 3)
        self.assertEqual(self.state.get_distance_between_fighters(), 3)
        
        self.state.set_fighter_position(self.f1, 1)
        self.state.set_fighter_position(self.f0, 3)
        self.state.set_fighter_position(self.f1, 0)
        self.assertEqual(self.state.get_distance_between_fighters(), 3)
        
        self.state.set_fighter_position(self.f0, 6)
        self.state.set_fighter_position(self.f1, 0)
        self.assertEqual(self.state.get_distance_between_fighters(), 6)
        
        
    def test_cannot_set_identical_fighter_positions(self):
        self.state.clear_fighter_positions()
        self.state.set_fighter_position(self.f0, 2)
        self.assertEqual(self.state.get_fighter_state(self.f0).get_position(), 2, "Initial fighter state was not set correctly.")
        with self.assertRaises(Exception) as context:
            self.state.set_fighter_position(self.f1, 2)
            
            
    def test_unable_to_find_active_fighter_when_active_fighter_not_set(self):
        with self.assertRaises(Exception) as context:
            self.state.get_active_fighter()
    
    
    def test_unable_to_find_reactive_fighter_when_active_fighter_not_set(self):
        with self.assertRaises(Exception) as context:
            self.state.get_reactive_fighter()
    
    
    def test_unable_to_find_reactive_fighter_when_only_one_fighter_exists(self):
        self.state = game_state.GameState(self.f0, self.f0)
        self.state.set_active_fighter(self.f0)
        with self.assertRaises(Exception) as context:
            self.state.get_reactive_fighter()
    
        

if __name__ == "__main__":
    unittest.main()
