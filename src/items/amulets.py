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
        v = rand(1, 4) 
        if v == 1:
            if self.suffix("wind"):
                self.modifier += Mod('speed', 1)
        elif v == 2:
            if self.suffix("sun"):
                self.modifier += Mod('radius', 1)
        elif v == 3:
            if self.suffix("wolf"):
                self.modifier += AddMaxLife(rand(3, 9))
        else:
            if self.suffix("spirit"):
                self.modifier += AddMaxMana(rand(5, 11))

class WispAmulet(Amulet):
    name = 'amulet'
    dungeons = 5, 8
    rarity = 15
    
    def __init__(self):
        super().__init__()
        v = rand(1, 3) 
        if v == 1:
            if self.suffix("reflections"):
                self.modifier += Mod('reflect_damage_bonus', 25)
        elif v == 2:
            if self.suffix("tiger"):
                self.modifier += AddMaxLife(rand(10, 24))
        else:
            if self.suffix("star"):
                self.modifier += AddMaxMana(rand(12, 29))

class WardAmulet(Amulet):
    name = 'amulet'
    dungeons = 9, 12
    rarity = 20
    
    def __init__(self):
        super().__init__()
        v = rand(1, 3) 
        if v == 1:
            if self.suffix("mirros"):
                self.modifier += Mod('reflect_damage_bonus', 50)
        elif v == 2:
            if self.suffix("whale"):
                self.modifier += AddMaxLife(rand(25, 45))
        else:
            if self.suffix("rainbow"):
                self.modifier += AddMaxMana(rand(30, 50))

class RubyAmulet(Amulet):
    ABSTRACT = True
    name = 'ruby amulet'
    art = 'ruby_amulet'
    glyph = '\'', T.red
    magical = True

    def __init__(self):
        super().__init__()
        self.modifier += AddMaxLife(75)


       

