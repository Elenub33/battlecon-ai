import unittest
from src.fighters.fighter_loader import FighterLoader

class TestFighterLoader(unittest.TestCase):
    
    
    expected_fighters = set([
        "Eligor Larington",
        "Shekhtur Lenmorre"
    ])
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        pass
        
        
    def test_get_fighter_list_does_not_contain_fighter(self):
        modules_and_classes = FighterLoader.get_fighter_module_class_pairs()
        for module, cls in modules_and_classes:
            self.assertFalse("fighter" in module, "Fighter was contained in {}.".format(modules_and_classes))
        
        
    def test_get_fighter_list_contains_fighters(self):
        modules_and_classes = FighterLoader.get_fighter_module_class_pairs()
        found_fighters = set()
        for module, cls in modules_and_classes:
            found_fighters.add(cls.get_full_name())
        self.assertTrue(TestFighterLoader.expected_fighters.issubset(found_fighters), "Some fighters from {} were not returned by fighter loader ({}).".format(TestFighterLoader.expected_fighters, found_fighters))
        

if __name__ == "__main__":
    print("TESTING")
    unittest.main()


