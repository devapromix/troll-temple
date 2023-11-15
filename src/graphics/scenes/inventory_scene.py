import pygame
import tcod as T

from common.game import out_file, out, GAME
from common.utils import *
from graphics.color import Color
from graphics.scenes.selection_scene import SelectionScene

class InventoryScene(SelectionScene):
    def __init__(self, player):
        super().__init__("INVENTORY Press [ENTER] to use, [TAB] to drop, [ESC] to exit", player.items, True)
        self.player = player

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
        if self.player.has_equipped(item):
            color = self._item_color(item, Color.SELECT.value)
            out(2, y, '*', color)
        if item == self.selected:
            self._draw_item(x, y, c, s, Color.SELECT.value)
        else:
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
                    self.player.use(item)
                    self.exit()
            return True
        
        if key == pygame.K_ESCAPE:
            self.exit()
            return True
        
        if key == pygame.K_TAB:
            if self.focusable:
                item = self.selected
                if item:
                    self.player.drop(item)
                    self.exit()
            return True
        
        return False
            