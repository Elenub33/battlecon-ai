import unittest
import src.agent as agent, src.fighters.fighter as fighter

class TestGame(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.fighter = fighter.Fighter()
        self.agent = agent.Agent(self.fighter)
        
        
    def test_get_fighter(self):
        self.assertEqual(self.fighter, self.agent.get_fighter(), "agent.get_fighter() did not return the fighter passed during initialization.")
        

if __name__ == "__main__":
    unittest.main()
