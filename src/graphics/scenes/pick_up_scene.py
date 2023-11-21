import pygame
import tcod as T

from common.game import out_file, out, GAME
from common.utils import *
from graphics.color import Color
from graphics.scenes.selection_scene import SelectionScene

class PickUpScene(SelectionScene):
    def __init__(self, player, tile):
        super().__init__("Press [ENTER] to pick up, [ESC] to exit", tile.items, True)
        self.player = player
        self.tile = tile
        self.has_footer = False

    def _item_color(self, item, color):
        if item.color != Color.ITEM.value:
            return item.color
        else:
            return color

    def _draw_item(self, x, y, c, s, color):
        out(x, y, c, color)
        out(x + 2, y, s, color)

    def _draw_item_name(self, x: int, y: int, item: object) -> None:
        c, color = item.glyph
        s = item.descr
        self._draw_item(x, y, c, s, color)

    def _draw_selected_info(self, item: object) -> None:
        out_file(81, 1, '../assets/texts/' + item.art + '.txt', item.glyph[1])

    def _check_input(self, key: int) -> bool:
        from common.game import pygame
        if super()._check_input(key, False):
            return True
            
        if key == pygame.K_RETURN:
            if self.focusable:
                item = self.selected
                if item:
                    self.player.pick_up(item)
                    self.exit()
            return True
        
        if key == pygame.K_ESCAPE:
            self.exit()
            return True
        
        return False





















