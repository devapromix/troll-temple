from graphics.color import Color
from mobs.abilities.ability import Ability

class ConjureManaOrb(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        super().__init__(player)
        self.game_class = Classes.MAGE
        self.need_mana = 15
        
    def use(self):
        from items.mana_orb import ManaOrb
        from common.game import message
        if super().use():
            return
        message('You have conjure a mana orb.')
        self.player.mana.modify(-self.need_mana)
        self.player.tile.items.append(ManaOrb())
