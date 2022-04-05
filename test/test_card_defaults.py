import unittest
import src.fighters.elements.defaults as defaults
import src.fighters.elements.base as base
import src.fighters.elements.style as style

class TestCardDefaults(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        pass
        
        
    def test_get_default_bases(self):
        default_bases = defaults.get_default_bases()
        classes = set()
        self.assertEqual(len(default_bases), 6, "Incorrect number of bases returned.")
        for b in default_bases:
            self.assertTrue(isinstance(b, base.Base), "{} was not a base.".format(b))
            classes.add(type(b))
        self.assertEqual(len(default_bases), 6, "Incorrect number of bases returned.")
        self.assertEqual(len(classes), 6, "Incorrect number of different bases returned.")
        
        
    def test_get_default_styles(self):
        default_styles = defaults.get_default_styles()
        for s in default_styles:
            self.assertTrue(isinstance(s, style.Style), "{} was not a style.".format(s))
        self.assertEqual(len(default_styles), 1, "Incorrect number of styles returned.")
        

if __name__ == "__main__":
    unittest.main()