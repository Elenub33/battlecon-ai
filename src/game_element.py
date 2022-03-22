"""
Any element that can affect an attack.
"""
class GameElement:
    
    
    def __init__(self):
        self.name = "???"
        self.min_range = 0
        self.max_range = 0
        
        
    def get_min_range(self):
        return self.min_range
        
        
    def get_max_range(self):
        return self.max_range