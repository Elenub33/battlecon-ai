import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
import random
import agent_yaron

class TestOttavia(unittest.TestCase):


    def setUp(self):
        random.seed(0)


    """
    Plays a full game of battlecon, Ottavia vs. Rexan.
    On build 2411827684b and before, this test exposes a bug:
    TypeError: '<' not supported between instances of 'NoneType' and 'int'.
    """
    def test_ottaviaVsRexan(self):
        agent0 = agent_yaron.YaronAgent("ottavia")
        agent1 = agent_yaron.YaronAgent("rexan")
        game = battlecon.Game.from_start(agent0, agent1)
        log, winner = game.play_game()
    

if __name__ == "__main__":
    unittest.main()
