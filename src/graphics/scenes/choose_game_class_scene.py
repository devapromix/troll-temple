import pygame
import tcod as T
from common.utils import *
from graphics.color import Color

class ChooseGameClassScene:
    def __init__(self, game):
        self.game = game

    def show(self):
        self.draw()
        self.select()

    def draw(self):
        from common.game import clear, out_file, refresh, out, anykey, draw_statistics
        from mobs.player import GAME_CLASSES

        from mobs.player import GAME_CLASSES
        clear()
        out(2, 1, "Choose your class", Color.TITLE.value)
        for i, game_class in enumerate(GAME_CLASSES):
            out(3, i + 3, chr(i + ord('a')), Color.ITEM.value)
            if self.game.selected_game_class.value == i + 1:
                out(1, i + 3, '>', T.white)
                out(5, i + 3, game_class[0], T.white)
                out_file(20, 3, '../assets/texts/class_' + game_class[0].lower() +'.txt', Color.ITEM.value)
                out_file(70, 14, '../assets/texts/' + game_class[3].lower() +'.txt', game_class[2])
            else:
                out(5, i + 3, game_class[0], game_class[2])
        out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)

        refresh()

    def select(self):
        from mobs.player import GAME_CLASSES
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.event.clear()
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key in range(pygame.K_a, pygame.K_z):
                        i = event.key - pygame.K_a
                        if 0 <= i < len(GAME_CLASSES):
                            self.game.selected_game_class = GAME_CLASSES[i][1]
                            self.draw()
                    if pygame.key.get_pressed()[pygame.K_RETURN]:
                        pygame.event.clear()
                        return






























