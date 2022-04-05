import src.fighters.elements.element as element

"""
Includes attack pair, ante, and any other data associated with an attack.
"""
class AttackStrategy:
    
    
    def __init__(self, *elements: list[element.Element]):
        self.elements = set(elements)
        
        
    def get_elements(self):
        return self.elements
        
        
    def add_elements(self, *elements: list[element.Element]):
        for elt in elements:
            self.elements.add(elt)
            
            
    def get_min_range(self) -> int:
        return sum([elt.get_min_range() for elt in self.elements])
            
            
    def get_max_range(self) -> int:
        return sum([elt.get_max_range() for elt in self.elements])
        
        
    def get_range(self) -> (int, int):
        return (self.get_min_range(), self.get_max_range())