import os.path, glob, inspect, sys
import src.fighters.fighter as fighter


class FighterLoader:
    
    
    @staticmethod
    def from_name(name):
        return Fighter
        
        
    @staticmethod
    def get_fighter_module_class_pairs():
        module_names = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")) if os.path.isfile(f) and not f.endswith('__init__.py')]
        result = []
        for name in module_names:
            cls = FighterLoader.get_class_from_module(name)
            if issubclass(cls, fighter.Fighter) and not cls == fighter.Fighter:
                result.append((name, cls))
        
        return result

    
    @staticmethod
    def get_class_from_module(module_name):
        module_name = "src.fighters.{}".format(module_name)
        __import__(module_name)
        class_members = inspect.getmembers(sys.modules[module_name], inspect.isclass)
        return class_members[0][1]