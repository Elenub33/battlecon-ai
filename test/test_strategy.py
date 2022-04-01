import unittest
import src.game_element as game_element, src.strategy as strategy

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
        itm0 = game_element.GameElement()
        itm1 = game_element.GameElement()
        itm2 = game_element.GameElement()
        itm3 = game_element.GameElement()
        expected = set([itm0, itm1])
        strat = strategy.AttackStrategy(itm0, itm1)
        self.assertEqual(strat.get_elements(), expected, "Elements initialized into strategy could not be retrieved.")
        strat.add_elements(itm2)
        strat.add_elements(itm3)
        expected.add(itm2)
        expected.add(itm3)
        self.assertEqual(strat.get_elements(), expected, "Elements added to strategy could not be retrieved.")
        
    
    def test_get_min_range(self):
        elt0 = game_element.GameElement()
        elt1 = game_element.GameElement()
        elt0.min_range = 1
        elt1.min_range = 2
        strat = strategy.AttackStrategy(elt0, elt1)
        self.assertEqual(strat.get_min_range(), 3)
        
    
    def test_get_max_range(self):
        elt0 = game_element.GameElement()
        elt1 = game_element.GameElement()
        elt0.max_range = 2
        elt1.max_range = 3
        strat = strategy.AttackStrategy(elt0, elt1)
        self.assertEqual(strat.get_max_range(), 5)
        

if __name__ == "__main__":
    unittest.main()
