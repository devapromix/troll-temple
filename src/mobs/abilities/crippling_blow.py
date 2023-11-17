from graphics.color import Color
from mobs.abilities.ability import Ability

class CripplingBlow(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        super().__init__(player)
        self.game_class = Classes.RANGER
        self.need_mana = 4
        
    def use(self):
        from common.game import message, MIN_SPEED, look_mode
        if super().use():
            return
        mob = look_mode(True)
        if mob:
            mob.speed = MIN_SPEED
            self.player.mana.modify(-self.need_mana)
            message("You slowed down the %s" % mob.name)


            

        
        
        