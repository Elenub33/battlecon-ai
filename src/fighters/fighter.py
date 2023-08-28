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
        self._fighter = fighter
        self.set_position(-1)
        self.set_stunned(False)
        self.set_attack_strategy(None)
        self.set_life(20)
        
        
    def set_position(self, position: int):
        self._position = position
        
        
    def get_position(self) -> int:
        return self._position
        
        
    def set_stunned(self, stunned: bool):
        self._stunned = stunned
        
        
    def is_stunned(self) -> bool:
        return self._stunned
        
        
    def get_fighter(self) -> Fighter:
        return self._fighter
        
        
    def set_attack_strategy(self, strategy):
        self._strategy = strategy
        
        
    def get_attack_strategy(self):
        return self._strategy
        
        
    def clear_attack_strategy(self):
        self._strategy = None


    def set_life(self, life:int):
        self._life = life


    def get_life(self) -> int:
        return self._life
        