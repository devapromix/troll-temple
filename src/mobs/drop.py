from items.items import *
from common.utils import random_by_level

class AdvDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        if self.mob.map.player.has_life_adv_drop:
            self.mob.tile.items.append(HealingPotion())
        if self.mob.map.player.has_mana_adv_drop:
            self.mob.tile.items.append(ManaPotion())

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













