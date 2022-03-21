import card

"""
Includes attack pair, ante, and any other data associated with an attack.
"""
class AttackStrategy:
    
    
    def __init__(self, *elements):
        self.elements = set(elements)
        
        
    def get_elements(self):
        return self.elements
        
        
    def add_elements(self, *elements):
        for element in elements:
            self.elements.add(element)