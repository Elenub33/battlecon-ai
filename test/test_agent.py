import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import agent
import agent_yaron
import agent_human

class TestAgent(unittest.TestCase):
    
    
    def test_yaron_not_human(self):
        agt = agent_yaron.YaronAgent.from_fighter_name("Iri")
        self.assertFalse(agt.isHuman(), "YaronAgent is human.")
    
    
    def test_human_is_human(self):
        agt = agent_human.HumanAgent.from_fighter_name("Iri")
        self.assertTrue(agt.isHuman(), "HumanAgent is not human.")
        
        
    def test_agent_instantiates_fighter(self):
        agt = agent.Agent.from_fighter_name("Iri")
        self.assertTrue(isinstance(agt.get_fighter(), Iri))


if __name__ == "__main__":
    unittest.main()
