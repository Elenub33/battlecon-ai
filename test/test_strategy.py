import sys, os, unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import strategy

class TestStrategy(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        pass
        
        
    # """
    # Verify something
    # """
    def test_get_elements(self):
        itm0 = 6
        itm1 = "some string"
        itm2 = 6.31
        itm3 = 7.41
        expected = set([itm0, itm1])
        strat = strategy.AttackStrategy(itm0, itm1)
        self.assertEqual(strat.get_elements(), expected, "Elements initialized into strategy could not be retrieved.")
        strat.add_elements(itm2)
        strat.add_elements(itm3)
        expected.add(itm2)
        expected.add(itm3)
        self.assertEqual(strat.get_elements(), expected, "Elements added to strategy could not be retrieved.")
        

if __name__ == "__main__":
    unittest.main()
