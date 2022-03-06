import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
import random
import agent_yaron
import agent_learning

class TestLearningAgent(unittest.TestCase):


    """
    Plays one beat, Eligor vs. Shekhtur.
    """
    def test_eligorVsShekhtur(self):
        agent0 = agent_yaron.YaronAgent("shekhtur")
        agent1 = agent_learning.LearningAgent("eligor")
        game = battlecon.Game.from_start(agent0, agent1, first_beats=True)
        log, winner = game.play_game()
        print("WINNER: {} ({} vs. {})".format(winner, agent0.get_fighter().life, agent1.get_fighter().life))
    

if __name__ == "__main__":
    unittest.main()
