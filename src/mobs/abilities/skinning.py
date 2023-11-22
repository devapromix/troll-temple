from graphics.color import Color
from mobs.abilities.ability import Ability

class Skinning(Ability):
    def __init__(self, player):
        from mobs.player import Classes
        super().__init__(player)
        self.game_class = Classes.RANGER
        self.need_mana = 1
        
    def use(self):
        from items.corpse import Corpse
        from mobs.drop import SkinDrop
        from common.utils import rand
        from common.game import message
        if super().use():
            return
        tile = self.player.tile
        if tile.items == []:
            message('There is no corpse here to skin.', Color.ERROR.value)
        else:
            for item in tile.items:
                if isinstance(item, Corpse):
                    tile.items.remove(item)
                    self.player.mana.modify(-self.need_mana)
                    SkinDrop(self.player, item).drop()
                    message("You skinned a corpse.", Color.ALERT.value)
                    self.player.use_energy()
                    break
