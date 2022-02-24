import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import agent

class TestAgent(unittest.TestCase):
    
    
    def test_yaronIsNotHuman(self):
        agt = agent.YaronAgent()
        self.assertFalse(agt.isHuman(), "YaronAgent is human.")
    
    
    def test_humanIsHuman(self):
        agt = agent.HumanAgent()
        self.assertTrue(agt.isHuman(), "HumanAgent is not human.")


if __name__ == "__main__":
    unittest.main()
