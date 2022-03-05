import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
import random
import agent_yaron

class TestEligorVShekhtur(unittest.TestCase):


    """
    Plays a full game of battlecon, Eligor vs. Shekhtur.
    """
    def test_eligorVsShekhtur(self):
        agent0 = agent_yaron.YaronAgent("shekhtur")
        agent1 = agent_yaron.YaronAgent("eligor")
        game = battlecon.Game.from_start(agent0, agent1, first_beats=True)
        log, winner = game.play_game()
        print("WINNER:", winner)
    

if __name__ == "__main__":
    unittest.main()
