from .scene import Scene
from ..color import Color


class SelectionScene(Scene):
    def __init__(self, title, items: list, focusable: bool = False):
        super().__init__()
        self.items = items
        self.title = title
        self.focusable = focusable
        self.selected_index = 0 if self.focusable else None

    @property
    def selected(self):
        return self.items[self.selected_index] if self.selected_index is not None else None

    def _draw_content(self) -> None:
        from common.game import out
        out(2, 1, self.title, Color.TITLE.value)
        for i, item in enumerate(self.items):
            if self.focusable and self.selected_index == i:
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
                self.selected_index = i
                if not self.focusable:
                    self.exit()
            return True

        if self.selected is not None:
            if key == pygame.K_UP:
                self.selected_index = self.selected_index - 1 if self.selected_index != 0 else len(self.items) - 1
                return True
            if key == pygame.K_DOWN:
                self.selected_index = self.selected_index + 1 if self.selected_index != len(self.items) - 1\
                    else 0
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

