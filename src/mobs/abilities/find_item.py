from graphics.color import Color
from mobs.abilities.ability import Ability

class FindItem(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        super().__init__(player)
        self.game_class = Classes.FIGHTER
        self.need_mana = 2
        
    def use(self):
        from items.corpse import Corpse
        from mobs.drop import AdvDrop
        from common.utils import rand
        from common.game import message
        if super().use():
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
