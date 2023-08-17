import unittest
from src.agent import Agent
from src.fighters.fighter import Fighter

class TestGame(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.fighter = Fighter()
        self.agent = Agent(self.fighter)
        
        
    def test_get_fighter(self):
        self.assertEqual(self.fighter, self.agent.get_fighter(), "agent.get_fighter() did not return the fighter passed during initialization.")
        

if __name__ == "__main__":
    unittest.main()
