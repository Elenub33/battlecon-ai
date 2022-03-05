import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import agent_yaron

class TestYaronAgent(unittest.TestCase):
    
    
    def test_yaron_not_human(self):
        agt = agent_yaron.YaronAgent("Iri")
        self.assertFalse(agt.is_human(), "YaronAgent is human.")


if __name__ == "__main__":
    unittest.main()
