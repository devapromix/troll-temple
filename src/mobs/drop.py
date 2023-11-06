from items.items import *

class AdvDrop():
    def __init__(self, mob):
        self.mob = mob
        
    def drop(self):
        if self.mob.map.player.has_life_adv_drop:
            self.mob.tile.items.append(HealingPotion())
        if self.mob.map.player.has_mana_adv_drop:
            self.mob.tile.items.append(ManaPotion())
