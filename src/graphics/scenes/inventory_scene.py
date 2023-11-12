import pygame
import tcod as T

from common.game import out_file, out, GAME
from common.utils import *
from graphics.color import Color
from graphics.scenes.selection_scene import SelectionScene

class InventoryScene(SelectionScene):
    def __init__(self, game):
        super().__init__("Select an item", GAME.player.items, True)
        self.game = game

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
        k = ''
        if GAME.player.has_equipped(item):
            color = self._item_color(item, Color.SELECT.value)
            out(2, y, '*', color)
        if item == self.selected:
            self._draw_item(x, y, c, s, Color.SELECT.value)
        else:
            self._draw_item(x, y, c, s, color)

    def _draw_selected_info(self, item: object) -> None:
        pass
