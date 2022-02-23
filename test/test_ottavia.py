import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import battlecon
import random
import fighters


class TestOttavia(unittest.TestCase):


    def setUp(self):
        random.seed(0)


    """
    On build 2411827684b and before, this test exposes a bug:
    TypeError: '<' not supported between instances of 'NoneType' and 'int'.
    """
    def test_EvenlySizedChunks(self):
        base = "alpha"
        p1 = "ottavia"
        p2 = "rexan"
        game = battlecon.Game.from_start(p1, p2, base, base, default_discards=True)
        game.play_game()
    

if __name__ == "__main__":
    unittest.main()
