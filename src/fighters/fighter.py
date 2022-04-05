

class Fighter:


    def __init__(self):
        pass
        
        
    @classmethod
    def get_full_name(cls):
        raise NotImplementedError()
        
        
    @classmethod
    def get_nickname(cls):
        raise NotImplementedError()


class FighterState:


    def __init__(self, fighter: Fighter):
        self.fighter = fighter
        self.set_position(-1)
        self.set_stunned(False)
        self.set_attack_strategy(None)
        
        
    def set_position(self, position: int):
        self.position = position
        
        
    def get_position(self) -> int:
        return self.position
        
        
    def set_stunned(self, stunned: bool):
        self.stunned = stunned
        
        
    def is_stunned(self) -> bool:
        return self.stunned
        
        
    def get_fighter(self) -> Fighter:
        return self.fighter
        
        
    def set_attack_strategy(self, strategy):
        self.strategy = strategy
        
        
    def get_attack_strategy(self):
        return self.strategy
        
        
    def clear_attack_strategy(self):
        self.strategy = None
        