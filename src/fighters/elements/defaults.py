import src.fighters.elements.base as base
import src.fighters.elements.style as style


def get_default_bases():
    return [
        Strike(),
        Drive(),
        Grasp(),
        Burst(),
        Shot(),
        Dodge()
    ]
    
    
def get_default_styles():
    return [
        Switch()
    ]
    
    
class Strike(base.Base):
    pass
    
    
class Drive(base.Base):
    pass
    
    
class Grasp(base.Base):
    pass
    
    
class Burst(base.Base):
    pass
    
    
class Shot(base.Base):
    pass
    
    
class Dodge(base.Base):
    pass
    
    
class Switch(style.Style):
    pass