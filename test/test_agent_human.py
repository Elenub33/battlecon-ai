import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
import agent
import agent_human

class TestHumanAgent(unittest.TestCase):
    
    
    def setUp(self):
        self.ai = agent.Agent("shekhtur")
        self.human = agent_human.HumanAgent("eligor")
    
    
    def test_human_is_human(self):
        self.assertTrue(self.human.is_human(), "HumanAgent is not human.")
        
       
    @unittest.skip("can we isolate the choose_strategy() method better? this incomplete approach requires parsing a lot of unrelated data")
    def test_choose_strategy(self):
        game = battlecon.Game.from_start(self.ai, self.human, first_beats=True)
        game.play_game()
        # game.initialize_simulations()
        # game.reporting = False
        # game.simulate_beat() # slow
        # game.solve() # slow
        # self.human.choose_strategy()
        # game = battlecon.play_start_beat(self.ai, self.human)


if __name__ == "__main__":
    unittest.main()
