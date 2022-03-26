"""
Any element that can affect an attack.
"""
class GameElement:
    
    
    def __init__(self):
        self.set_name("???")
        self.set_min_range(0)
        self.set_max_range(0)
        
        
    def set_name(self, name):
        self.name = name
        
        
    def get_name(self):
        return self.name
        
        
    def set_min_range(self, min_range):
        self.min_range = min_range
        
        
    def get_min_range(self):
        return self.min_range
        
        
    def set_max_range(self, max_range):
        self.max_range = max_range
        
        
    def get_max_range(self):
        return self.max_range