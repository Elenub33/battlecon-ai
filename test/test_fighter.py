import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import fighter, strategy

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
        

if __name__ == "__main__":
    unittest.main()
