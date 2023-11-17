import tcod as T

from common.modifiers.mod import Mod
from items.Equipment import Equipment
from common.modifiers.attrib_mod import *

class Amulet(Equipment):
    ABSTRACT = True
    slot = 'n'
    art = 'amulet'
    glyph = '\'', T.gold
    magical = True

class RubyAmulet(Amulet):
    ABSTRACT = True
    name = 'ruby amulet'
    art = 'ruby_amulet'
    glyph = '\'', T.red
    magical = True

    def __init__(self):
        super().__init__()
        self.modifier += AddMaxLife(75)


class MirrorAmulet(Amulet):
    name = 'mirror amulet'
    art = 'mirror_amulet'
    glyph = '\'', T.green
    magical = True
    dungeons = 10, 12
    rarity = 20

    def __init__(self):
        super().__init__()
        self.modifier += Mod('reflect_damage_bonus', 75)

