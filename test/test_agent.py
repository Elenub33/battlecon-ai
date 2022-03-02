import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import agent
import agent_yaron
import agent_human

class TestAgent(unittest.TestCase):
    
    
    def test_yaron_not_human(self):
        agt = agent_yaron.YaronAgent("Iri")
        self.assertFalse(agt.is_human(), "YaronAgent is human.")
    
    
    def test_human_is_human(self):
        agt = agent_human.HumanAgent("Iri")
        self.assertTrue(agt.is_human(), "HumanAgent is not human.")


if __name__ == "__main__":
    unittest.main()
