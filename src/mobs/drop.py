from items.items import *
from items.keys import *
from items.amulets import *
from items.light_sources import *
from common.utils import random_by_level, rand


class SimpleDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        v = rand(1, 21)
        if v in range(1, 10):
            self.mob.tile.items.append(Torch())
        elif v in range(11, 20):
            if self.mob.map.level in range(1, 3):
                self.mob.tile.items.append(Torch())
            elif self.mob.map.level in range(4, 6):
                self.mob.tile.items.append(CopperLamp())
            elif self.mob.map.level in range(7, 9):
                self.mob.tile.items.append(BronzeLamp())
            elif self.mob.map.level in range(10, 12):
                self.mob.tile.items.append(SilverLamp())
        else:
            if self.mob.map.level == 1:
                self.mob.tile.items.append(CopperKey())
            elif self.mob.map.level in range(2, 4):
                self.mob.tile.items.append(SilverKey())
            elif self.mob.map.level in range(5, 8):
                self.mob.tile.items.append(GoldenKey())
            elif self.mob.map.level in range(9, 11):
                self.mob.tile.items.append(RunedKey())

class JewelryDrop():
    def __init__(self, mob):
        self.mob = mob

    def drop(self):
        if self.mob.map.level in range(1, 4):
            self.mob.tile.items.append(RavenAmulet())
        elif self.mob.map.level in range(5, 8):
            self.mob.tile.items.append(WispAmulet())
        elif self.mob.map.level in range(9, 12):
            self.mob.tile.items.append(WardAmulet())
        

class AdvDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        v = rand(1, 21)
        if v in range(1, 10):
            if self.mob.map.player.has_life_adv_drop:
                self.mob.tile.items.append(HealingPotion())
            if self.mob.map.player.has_mana_adv_drop:
                self.mob.tile.items.append(ManaPotion())
        elif v in range(11, 20):
            SimpleDrop(self.mob).drop()
        else:
            JewelryDrop(self.mob).drop()

class SkinDrop():
    def __init__(self, mob, corpse):
        self.mob = mob
        self.corpse = corpse

    def drop(self):
        from items.leather import Leather
        if self.corpse.has_skin:
            self.mob.tile.items.append(Leather())

class Drop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        item = random_by_level(self.mob.map.level, Item.ALL)()
        self.mob.tile.items.append(item)

class RareDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        item = random_by_level(self.mob.map.level, Item.ALL)()
        self.mob.tile.items.append(item)

class UniqueDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        item = random_by_level(self.mob.map.level, Item.ALL)()
        self.mob.tile.items.append(item)













