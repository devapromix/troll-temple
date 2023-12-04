import tcod as T
from items.Equipment import Equipment
from common.modifiers.mod import Mod
from common.utils import rand
from common.modifiers.attrib_mod import *

class Amulet(Equipment):
    ABSTRACT = True
    slot = 'n'
    art = 'amulet'
    glyph = '\'', T.gold

class RavenAmulet(Amulet):
    name = 'amulet'
    ABSTRACT = True
    
    def __init__(self):
        super().__init__()
        v = rand(1, 4) 
        if v == 1:
            if self.suffix("wind"):
                self.modifier += Mod('speed', 1)
                self.glyph = '\'', T.white
        elif v == 2:
            if self.suffix("sun"):
                self.modifier += Mod('radius', 1)
                self.glyph = '\'', T.light_yellow
        elif v == 3:
            if self.suffix("wolf"):
                self.modifier += AddMaxLife(rand(3, 9))
                self.glyph = '\'', T.light_red
        else:
            if self.suffix("spirit"):
                self.modifier += AddMaxMana(rand(5, 11))
                self.glyph = '\'', T.light_blue

class WispAmulet(Amulet):
    name = 'amulet'
    ABSTRACT = True
    
    def __init__(self):
        super().__init__()
        v = rand(1, 3) 
        if v == 1:
            if self.suffix("reflections"):
                self.modifier += Mod('reflect_damage_bonus', 25)
                self.glyph = '\'', T.light_pink
        elif v == 2:
            if self.suffix("tiger"):
                self.modifier += AddMaxLife(rand(10, 24))
                self.glyph = '\'', T.light_red
        else:
            if self.suffix("star"):
                self.modifier += AddMaxMana(rand(12, 29))
                self.glyph = '\'', T.light_blue

class WardAmulet(Amulet):
    name = 'amulet'
    ABSTRACT = True
    
    def __init__(self):
        super().__init__()
        v = rand(1, 3) 
        if v == 1:
            if self.suffix("mirros"):
                self.modifier += Mod('reflect_damage_bonus', 50)
                self.glyph = '\'', T.light_pink
        elif v == 2:
            if self.suffix("whale"):
                self.modifier += AddMaxLife(rand(25, 45))
                self.glyph = '\'', T.light_red
        else:
            if self.suffix("rainbow"):
                self.modifier += AddMaxMana(rand(30, 50))
                self.glyph = '\'', T.light_blue

class RubyAmulet(Amulet):
    ABSTRACT = True
    name = 'ruby amulet'
    art = 'ruby_amulet'
    glyph = '\'', T.red
    magical = True

    def __init__(self):
        super().__init__()
        self.modifier += AddMaxLife(75)


       

