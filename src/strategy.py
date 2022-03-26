import game_element

"""
Includes attack pair, ante, and any other data associated with an attack.
"""
class AttackStrategy:
    
    
    def __init__(self, *elements: list[game_element.GameElement]):
        self.elements = set(elements)
        
        
    def get_elements(self):
        return self.elements
        
        
    def add_elements(self, *elements: list[game_element.GameElement]):
        for element in elements:
            self.elements.add(element)
            
            
    def get_min_range(self) -> int:
        return sum([element.get_min_range() for element in self.elements])
            
            
    def get_max_range(self) -> int:
        return sum([element.get_max_range() for element in self.elements])
        
        
    def get_range(self) -> (int, int):
        return (self.get_min_range(), self.get_max_range())