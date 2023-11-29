import tcod as T

from common.modifiers.mod import Mod
from common.utils import rand
from items.Equipment import Equipment
from common.modifiers.attrib_mod import *

class Amulet(Equipment):
    ABSTRACT = True
    slot = 'n'
    art = 'amulet'
    glyph = '\'', T.gold

class RavenAmulet(Amulet):
    name = 'amulet'
    dungeons = 1, 4
    rarity = 10
    
    def __init__(self):
        super().__init__()
        v = rand(1, 3) 
        if v == 1:
            if self.suffix("wind"):
                self.modifier += Mod('speed', 1)
        elif v == 2:
            if self.suffix("wolf"):
                self.modifier += AddMaxLife(rand(3, 5))
        else:
            if self.suffix("sun"):
                self.modifier += AddMaxMana(rand(5, 9))

class WispAmulet(Amulet):
    name = 'amulet'
    dungeons = 5, 8
    rarity = 15
    
    def __init__(self):
        super().__init__()
        v = rand(1, 3) 
        if v == 1:
            if self.suffix("mirros"):
                self.modifier += Mod('reflect_damage_bonus', 25)
        elif v == 2:
            if self.suffix("tiger"):
                self.modifier += AddMaxLife(rand(10, 25))
        else:
            if self.suffix("star"):
                self.modifier += AddMaxMana(rand(12, 30))

class RubyAmulet(Amulet):
    ABSTRACT = True
    name = 'ruby amulet'
    art = 'ruby_amulet'
    glyph = '\'', T.red
    magical = True

    def __init__(self):
        super().__init__()
        self.modifier += AddMaxLife(75)


       

