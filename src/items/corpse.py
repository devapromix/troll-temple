import tcod as T
from .Item import Item

class Corpse(Item):
    ABSTRACT = True
    glyph = "%", T.dark_orange
    
    def __init__(self, mob):
        self.name = mob.name + " corpse"
    
    
    
    