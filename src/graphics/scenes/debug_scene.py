from abc import abstractmethod

import pygame

from common.utils import Register
from graphics.scenes.scene import Scene


class DebugCommand(metaclass=Register):
    ALL = []
    ABSTRACT = True

    @abstractmethod
    def run(self, **kwargs):
        pass


class GetCommand(DebugCommand):
    def run(self, *args):
        item_name = args[0]

        import items.Item
        import items.items
        for item_class in items.Item.Item.ALL:
            if item_class.__name__.lower() == item_name.lower():
                from common.game import GAME
                GAME.player.items.append(item_class())

        pass


class DebugScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = ""

    def _draw_content(self) -> None:
        from common.game import out
        out(1, 1, self.text + "_")

    def _check_input(self, key: int) -> bool:
        if key == pygame.K_RETURN:
            self.__run_command()
            self.exit()
            return True
        name = pygame.key.name(key)
        if len(name) == 1:
            self.text += name
            return True
        if name == "space":
            self.text += ' '
            return True
        if name == "backspace":
            self.text = self.text[:-1]
            return True
        return False

    def __run_command(self) -> None:
        parsed = self.text.split(' ')
        for cmd_class in DebugCommand.ALL:
            if cmd_class.__name__.lower() == parsed[0].lower() + "command":
                cmd_class().run(*parsed[1:])
