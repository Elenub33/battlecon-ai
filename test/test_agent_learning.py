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
    @unittest.skip("Too long for now.")
    def test_eligor_v_shekhtur(self):
        log, winner = self.game.play_game()
        print("WINNER: {} ({} vs. {})".format(winner, self.yaron_agent.get_fighter().life, self.learning_agent.get_fighter().life))
    
    
    def test_get_self_range_from_edge(self):
        agt = self.learning_agent
        f = agt.get_fighter()
        expected_vals = [0,1,2,3,2,1,0]
        for pos, rg in enumerate(expected_vals):
            f.position = pos
            self.assertEqual(agt.get_range_from_edge(f), rg, "Unexpected edge range returned.")
    
    
    def test_get_opponent_range_from_edge(self):
        agt = self.learning_agent
        f = agt.get_fighter().opponent
        expected_vals = [0,1,2,3,2,1,0]
        for pos, rg in enumerate(expected_vals):
            f.position = pos
            self.assertEqual(agt.get_range_from_edge(f), rg, "Unexpected edge range returned.")
    
    
    def test_get_get_range_between_fighters(self):
        agt = self.learning_agent
        f = agt.get_fighter()
        o = f.opponent
        expected_vals = [
            (0, 1, 1),
            (0, 2, 2),
            (0, 3, 3),
            (0, 4, 4),
            (0, 5, 5),
            (0, 6, 6),
            (1, 0, 1),
            (1, 2, 1),
            (1, 3, 2),
            (1, 4, 3),
            (1, 5, 4),
            (1, 6, 5),
            (2, 0, 2),
            (2, 1, 1),
            (2, 3, 1),
            (2, 4, 2),
            (2, 5, 3),
            (2, 6, 4),
            (3, 0, 3),
            (3, 1, 2),
            (3, 2, 1),
            (3, 4, 1),
            (3, 5, 2),
            (3, 6, 3),
            (4, 0, 4),
            (4, 1, 3),
            (4, 2, 2),
            (4, 3, 1),
            (4, 5, 1),
            (4, 6, 2),
            (5, 0, 5),
            (5, 1, 4),
            (5, 2, 3),
            (5, 3, 2),
            (5, 4, 1),
            (5, 6, 1),
            (6, 0, 6),
            (6, 1, 5),
            (6, 2, 4),
            (6, 3, 3),
            (6, 4, 2),
            (6, 5, 1)
        ]
        for f_pos, o_pos, rg in expected_vals:
            f.position = f_pos
            o.position = o_pos
            self.assertEqual(agt.get_range_between_fighters(), rg, "Unexpected opponent range returned for positions {} and {}.".format(f_pos, o_pos))
    

if __name__ == "__main__":
    unittest.main()
