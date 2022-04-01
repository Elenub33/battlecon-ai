import unittest
import src.fighters.fighter_loader as fighter_loader

class TestFighterLoader(unittest.TestCase):
    
    
    """
    Prepare the test case.
    """
    def setUp(self):
        pass
        
        
    def test_get_fighter_list_does_not_contain_fighter(self):
        modules_and_classes = fighter_loader.FighterLoader.get_fighter_module_class_pairs()
        for module, cls in modules_and_classes:
            self.assertFalse("fighter" in module, "Fighter was contained in {}.".format(modules_and_classes))
        
        
    def test_get_fighter_list_cotnains_eligor(self):
        expected_class_name = "Eligor Larington"
        modules_and_classes = fighter_loader.FighterLoader.get_fighter_module_class_pairs()
        found = False
        for module, cls in modules_and_classes:
            if cls.get_full_name() == expected_class_name:
                found = True
        self.assertTrue(found, "{} was not returned in {}.".format(expected_class_name, modules_and_classes))
        

if __name__ == "__main__":
    unittest.main()


