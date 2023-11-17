class Ability:
    def __init__(self, player):
        from mobs.player import Classes
        self.player = player
        self.game_class = Classes.FIGHTER
        self.need_mana = 2

    def use(self):
        from mobs.player import GAME_CLASSES
        from graphics.color import Color
        from common.game import message
        if self.player.game_class != self.game_class:
            message("Only a %s can use this ability!" % GAME_CLASSES[self.game_class.value - 1][0], Color.ERROR.value)
            return True
        if self.player.mana.cur < self.need_mana:
            message("Need more mana!", Color.ERROR.value)
            return True
        return False

