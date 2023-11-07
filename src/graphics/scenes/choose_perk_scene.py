from graphics.color import Color
from graphics.scenes.selection_scene import SelectionScene
from mobs.perks.perks import *
import tcod as T


class ChoosePerkScene(SelectionScene):
    RARITY_COLORS = {
        PerkRarity.USUALLY: T.light_grey,
        PerkRarity.RARE: T.lighter_blue,
        PerkRarity.LEGEND: T.lighter_red,
    }

    def __init__(self, player):
        super().__init__("Choose your destiny", player.perks.generate_new_perks(), True)
        self.__player = player

    def show(self):
        super().show()
        self.__player.perks.teach(self.selected)

    def _draw_item_name(self, x: int, y: int, item: Perk) -> None:
        from common.game import out
        out(x, y, item.name, self.RARITY_COLORS[item.rarity])

    def _draw_selected_info(self, item: Perk) -> None:
        from common.game import out
        DESCR_LINE_X = 25
        out(DESCR_LINE_X, 3, item.descr, Color.ITEM.value)
        out(DESCR_LINE_X, 5, item.modifier.descr, Color.MAGIC.value)
