import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
import random
import agent_yaron
import agent_learning

class TestLearningAgent(unittest.TestCase):

    
    def setUp(self):
        self.yaron_agent = agent_yaron.YaronAgent("shekhtur")
        self.learning_agent = agent_learning.LearningAgent("eligor")
        game = battlecon.Game.from_start(self.yaron_agent, self.learning_agent, first_beats=True)
        

    """
    Plays one beat, Eligor vs. Shekhtur.
    """
    def test_eligor_v_shekhtur(self):
        log, winner = self.game.play_game()
        print("WINNER: {} ({} vs. {})".format(winner, self.yaron_agent.get_fighter().life, self.learning_agent.get_fighter().life))
    

if __name__ == "__main__":
    unittest.main()
