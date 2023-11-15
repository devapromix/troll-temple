import tcod as T
from items.Equipment import Equipment
from common.modifiers.attrib_mod import *

class Amulet(Equipment):
    ABSTRACT = True
    slot = 'n'
    glyph = '\'', T.gold
    magical = True

class RubyAmulet(Amulet):
    ABSTRACT = True
    name = 'ruby amulet'
    glyph = '\'', T.red
    magical = True

    def __init__(self):
        super().__init__()
        self.modifier += AddMaxLife(75)

