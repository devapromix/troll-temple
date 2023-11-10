from .scene import Scene
from ..color import Color


class SelectionScene(Scene):
    def __init__(self, title, items: list, focusable: bool = False):
        super().__init__()
        self.items = items
        self.selected = None
        self.title = title
        self.focusable = focusable
        if self.focusable:
            self.selected = items[0]

    def _draw_content(self) -> None:
        from common.game import out
        out(2, 1, self.title, Color.TITLE.value)
        for i, item in enumerate(self.items):
            if self.focusable and self.selected == item:
                out(1, i + 3, '>', Color.ITEM.value)
                self._draw_selected_info(item)
            id = chr(i + ord('a'))
            out(3, i + 3, id, Color.ITEM.value)
            self._draw_item_name(5, i + 3, item)
        if self.focusable:
            out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)

    def _check_input(self, key: int) -> bool:
        from common.game import pygame

        if key in range(pygame.K_a, pygame.K_z):
            i = key - pygame.K_a
            if 0 <= i < len(self.items):
                self.selected = self.items[i]
                if not self.focusable:
                    self.exit()
            return True

        if key == pygame.K_RETURN:
            if self.focusable:
                self.exit()
            return True

        return False

    def _draw_item_name(self, x: int, y: int, item: object) -> None:
        from common.game import out
        out(x, y, str(item), Color.MAGIC.value)

    def _draw_selected_info(self, item: object) -> None:
        pass

