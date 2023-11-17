from graphics.color import Color

class FindItem(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        self.player = player
        self.game_class = Classes.FIGHTER
        self.need_mana = 2
        
    def use(self):
        from mobs.player import GAME_CLASSES
        from items.corpse import Corpse
        from mobs.drop import AdvDrop
        from common.utils import rand
        from common.game import message
        super().use()
        if self.player.game_class != self.game_class:
            message("Only a %s can use this ability!" % GAME_CLASSES[self.game_class], Color.ERROR.value)
            return
        if self.player.mana.cur < self.need_mana:
            message("Need more mana!", Color.ERROR.value)
            return
        tile = self.player.tile
        if tile.items == []:
            message('There is no corpse here to examine.', Color.ERROR.value)
        else:
            for item in tile.items:
                if isinstance(item, Corpse):
                    tile.items.remove(item)
                    self.player.mana.modify(-self.need_mana)
                    if rand(1, 4) == 1:
                        d = AdvDrop(self.player)
                        d.drop()
                        message("You found something.", Color.ALERT.value)
                    else:
                        message("You didn't find anything.", Color.ITEM.value)
                    self.player.use_energy()
                    break
