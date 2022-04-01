import unittest
import src.fighters.fighter as fighter, src.strategy as strategy

class TestFighter(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.fighter = fighter.Fighter()
        self.fighter_state = fighter.FighterState(self.fighter)
        
        
    def test_set_position(self):
        fs = self.fighter_state
        for p in range(0, 7):
            fs.set_position(p)
            self.assertEqual(fs.get_position(), p, "Fighter not set to position {}".format(p))
            
            
    def test_set_stunned(self):
        fs = self.fighter_state
        for val in (True, False):
            fs.set_stunned(val)
            self.assertEqual(fs.is_stunned(), val, "Stun state not set to {}.".format(val))
        
        
    def test_set_attack_strategy(self):
        fs = self.fighter_state
        strat = strategy.AttackStrategy()
        fs.set_attack_strategy(strat)
        self.assertEqual(fs.get_attack_strategy(), strat, "Strategy was not set.")
        
        
    def test_clear_attack_strategy(self):
        fs = self.fighter_state
        strat = strategy.AttackStrategy()
        fs.set_attack_strategy(strat)
        fs.clear_attack_strategy()
        self.assertEqual(fs.get_attack_strategy(), None, "Strategy was not cleared.")
        
        
    def test_get_fighter(self):
        self.assertEqual(self.fighter, self.fighter_state.get_fighter(), "get_fighter did not return the fighter passed to the __init__ function.")
        

if __name__ == "__main__":
    unittest.main()
