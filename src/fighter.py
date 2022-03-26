class Fighter:


    def __init__(self):
        pass


class FighterState:


    def __init__(self, fighter: Fighter):
        self.fighter = fighter
        self.set_position(-1)
        self.strategy = None
        
        
    def set_position(self, position: int):
        self.position = position
        
        
    def get_position(self) -> int:
        return self.position
        
        
    def get_fighter(self) -> Fighter:
        return self.fighter
        
        
    def set_attack_strategy(self, strategy):
        self.strategy = strategy
        
        
    def get_attack_strategy(self):
        return self.strategy
        
        
    def clear_attack_strategy(self):
        self.strategy = None