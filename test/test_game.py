import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon, fighters, agent

class TestGame(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.agent0 = agent.Agent("eligor")
        self.agent1 = agent.Agent("shekhtur")
        self.game = battlecon.Game.from_start(self.agent0, self.agent1)
    
    
    """
    Verify that the game can be initialized from start and sets up fighters correctly.
    """
    def test_game_from_start_initializes_agents(self):
        
        self.assertTrue(isinstance(self.agent0.get_fighter(), fighters.Eligor), "Unexpected fighter class.")
        self.assertTrue(isinstance(self.agent1.get_fighter(), fighters.Shekhtur), "Unexpected fighter class.")
        
        self.assertEqual(self.agent0.get_player_number(), 0, "Unexpected player number.")
        self.assertEqual(self.agent1.get_player_number(), 1, "Unexpected player number.")
        
        self.assertEqual(self.agent0.get_game(), self.game, "Unexpected game saved.")
        self.assertEqual(self.agent1.get_game(), self.game, "Unexpected game saved.")
        
        


if __name__ == "__main__":
    unittest.main()
