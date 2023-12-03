from items.items import *
from items.light_sources import *
from common.utils import random_by_level, rand


class SimpleDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        from items.keys import CopperKey, SilverKey, GoldenKey, RunedKey
        i = rand(1, 2)
        if i == 1:
            self.mob.tile.items.append(Torch())
        else:
            if self.mob.map.level == 1:
                self.mob.tile.items.append(CopperKey())
            elif self.mob.map.level in [2, 3, 4]:
                self.mob.tile.items.append(SilverKey())
            elif self.mob.map.level in [5, 6, 7, 8]:
                self.mob.tile.items.append(GoldenKey())
            elif self.mob.map.level in [9, 10, 11]:
                self.mob.tile.items.append(RunedKey())

class AdvDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        i = rand(1, 2)
        if i == 1:
            if self.mob.map.player.has_life_adv_drop:
                self.mob.tile.items.append(HealingPotion())
            if self.mob.map.player.has_mana_adv_drop:
                self.mob.tile.items.append(ManaPotion())
        else:
            SimpleDrop(self.mob).drop()

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













