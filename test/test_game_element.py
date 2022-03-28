import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import game_element

class TestGameElement(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        self.ge = game_element.GameElement()
        
        
    def test_set_name(self):
        ge = self.ge
        test_names = ["foobar", "SHAZBOT", "1235"]
        for name in test_names:
            ge.set_name(name)
            self.assertEqual(ge.get_name(), name)
    
    
    def test_set_min_range(self):
        ge = self.ge
        for rg in range(1,6):
            ge.set_min_range(rg)
            self.assertEqual(ge.get_min_range(), rg)
    
    def test_set_max_range(self):
        ge = self.ge
        for rg in range(1,6):
            ge.set_max_range(rg)
            self.assertEqual(ge.get_max_range(), rg)
        
        

if __name__ == "__main__":
    unittest.main()
