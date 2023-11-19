import pygame
import tcod as T

from graphics.window import *
from graphics.color import Color
from graphics.scenes.selection_scene import SelectionScene
from mobs.player import GAME_CLASSES


class ChooseGameClassScene(SelectionScene):
    def __init__(self, game):
        super().__init__("Choose your class", GAME_CLASSES, True)
        self.game = game

    def _draw_item_name(self, x: int, y: int, game_class: object) -> None:
        if game_class == self.selected:
            out(x, y, game_class[0], T.white)
        else:
            out(x, y, game_class[0], game_class[2])

    def _draw_selected_info(self, game_class: object) -> None:
        out_file(20, 3, '../assets/texts/class_' + game_class[0].lower() +'.txt', Color.ITEM.value)
        out_file(70, 14, '../assets/texts/' + game_class[3].lower() +'.txt', game_class[2])
