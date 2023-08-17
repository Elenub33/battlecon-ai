import os.path, glob, inspect, sys
from .fighter import Fighter


class FighterLoader:
    
    
    @staticmethod
    def from_name(name):
        return Fighter
        
        
    @staticmethod
    def get_fighter_module_class_pairs():
        module_names = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")) if os.path.isfile(f) and not f.endswith('__init__.py')]
        result = []
        for name in module_names:
            cls = FighterLoader.load_fighter_from_module(name)
            if cls != None:
                result.append((name, cls))
        
        return result

    
    @staticmethod
    def load_fighter_from_module(module_name):
        module_name = "src.fighters.{}".format(module_name)
        __import__(module_name)
        class_members = inspect.getmembers(sys.modules[module_name], inspect.isclass)
        for name, cls in class_members:
            if not cls == Fighter and issubclass(cls, Fighter):
                return cls
        return None