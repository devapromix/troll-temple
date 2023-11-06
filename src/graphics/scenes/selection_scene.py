from .scene import Scene
from ..color import Color


class SelectionScene(Scene):
    def __init__(self, title, items: list):
        self.items = items
        self.selected = None
        self.title = title

    def _draw_content(self) -> None:
        from common.game import out
        out(10, 1, self.title, Color.TITLE.value)
        for i, item in enumerate(self.items):
            id = chr(i + ord('a'))
            out(3, i + 3, id, Color.ITEM.value)
            out(5, i + 3, item.name, Color.MAGIC.value)

    def _check_input(self, key: int) -> bool:
        from common.game import pygame
        if key in range(pygame.K_a, pygame.K_z):
            i = key - pygame.K_a
            if 0 <= i < len(self.items):
                self.selected = self.items[i]
                return True
        return False

