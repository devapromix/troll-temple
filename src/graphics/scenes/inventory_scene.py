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

    def _slot_name(self, item):
        from common.game import INVENTORY_SLOTS
        r = ''
        if item.slot:
            for slot in INVENTORY_SLOTS:
                if item.slot in slot:
                    r = str(slot)
                    break
        return r

    def _item_color(self, item, color):
        if item.color != Color.ITEM.value:
            return item.color
        else:
            return color

    def _draw_item(self, x, y, c, s, k, color):
        out(x, y, c, color)
        out(x + 2, y, s + " " + k, color)

    def _draw_item_name(self, x: int, y: int, item: object) -> None:
        c, color = item.glyph
        s = item.descr
        k = ''
        if GAME.player.has_equipped(item):
            color = self._item_color(item, Color.SELECT.value)
            k = '- ' + self._slot_name(item)
        if item == self.selected:
            self._draw_item(x, y, c, s, k, Color.SELECT.value)
        else:
            self._draw_item(x, y, c, s, k, color)

    def _draw_selected_info(self, item: object) -> None:
        pass
