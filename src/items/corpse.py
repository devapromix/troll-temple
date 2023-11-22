import tcod as T
from .Item import Item

class Corpse(Item):
    ABSTRACT = True
    glyph = "%", T.dark_orange
    False
    
    def __init__(self, mob):
        self.name = mob.name + " corpse"
        self.has_skin = mob.has_skin
    
    
    