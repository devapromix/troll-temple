from graphics.color import Color
from mobs.abilities.ability import Ability

class Stealth(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        super().__init__(player)
        self.game_class = Classes.THIEF
        self.need_mana = 6
        
    def use(self):
        from mobs.player import Invisibility
        from common.game import message
        if self.player.invisibility != Invisibility.NONE:
            self.player.visibility()
            return
        if super().use():
            return
        if self.player.invisibility == Invisibility.NONE:
            self.player.invisibility = Invisibility.SHADOW
            message("You hide in the shadows!")
            self.player.mana.modify(-self.need_mana)

            

        
        
        