from abc import abstractmethod
from typing import List

import pygame

from common.utils import Register
from graphics.layout import Layout
from graphics.line import Line
from graphics.point import Point
from graphics.scenes.scene import Scene
import tcod as T


class DebugCommand(metaclass=Register):
    ALL = []
    ABSTRACT = True

    @abstractmethod
    def run(self, **kwargs):
        pass

    @abstractmethod
    def auto_complete_arg(self, value: str, index: int) -> List[str]:
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

    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        import items.Item
        import items.items
        return [cls.__name__ for cls in items.Item.Item.ALL if value.lower() in cls.__name__.lower()]


class SpawnCommand(DebugCommand):
    def run(self, *args):
        name = args[0]

        from mobs.monster import Monster
        import mobs.mobs
        for cls in Monster.ALL:
            if cls.__name__.lower() == name.lower():
                from common.game import GAME
                GAME.map.place_monsters(cls)

    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        from mobs.monster import Monster
        import mobs.mobs
        return [cls.__name__ for cls in Monster.ALL if value.lower() in cls.__name__.lower()]


class LevelUpCommand(DebugCommand):
    def run(self, *args):
        from common.game import GAME
        GAME.player.advance()

    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        return []


class DebugScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.args = []

    def _draw_content(self) -> None:
        from common.game import out, out_list

        auto_complete_list=[]
        line = Layout(Point(1, 0))
        for i, arg in enumerate(self.args):
            auto_complete_list = self.__auto_complete_list(i)
            lower_auto_complete_list = [x.lower() for x in auto_complete_list]
            line.print(arg, T.lighter_green if arg.lower() in lower_auto_complete_list else T.lighter_red)
            if i < len(self.args)-1:
                line.print(' ')
        line.print('_')

        if len(auto_complete_list) > 0:
            line.color = T.lighter_blue
            line.next()
            line.print(auto_complete_list[0], background_color=T.darker_grey)
            out_list(1, 2, auto_complete_list[1:], T.lighter_blue)

        from common.game import out_file
        out_file(50, 0, '../assets/texts/debug_help.txt', T.white)

    def _check_input(self, key: int) -> bool:
        if key == pygame.K_RETURN:
            command = self.__current_command
            if command is not None:
                self.__current_command.run(*self.args[1:])
            self.exit()
            return True
        if key == pygame.K_SPACE:
            self.text += ' '
            self.__parse()
            return True
        if key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            self.__parse()
            return True
        if key == pygame.K_TAB:
            self.__complete()
            return True

        name = pygame.key.name(key)
        if len(name) == 1:
            self.text += name
            self.__parse()
            return True
        return False

    @property
    def __current_command(self) -> DebugCommand:
        for cls in DebugCommand.ALL:
            if cls.__name__.lower() == self.args[0].lower() + "command":
                return cls()

    def __auto_complete_list(self, index: int) -> List[str]:
        if index > 0:
            return self.__auto_complete_list_arg(len(self.args) - 1)
        else:
            return self.__auto_complete_list_command

    @property
    def __auto_complete_list_command(self) -> List[str]:
        names = map(lambda x: x.__name__[:-len("command")], DebugCommand.ALL)
        return [x for x in names if self.args[0].lower() in x.lower()]

    def __auto_complete_list_arg(self, index: int) -> List[str]:
        command = self.__current_command
        names = command.auto_complete_arg(self.args[index], index - 1) if command is not None else []
        return [x for x in names if self.args[index].lower() in x.lower()]

    def __complete(self) -> None:
        auto_complete_list = self.__auto_complete_list(len(self.args) - 1)
        if len(auto_complete_list) > 0:
            self.args[-1] = auto_complete_list[0]
            self.__deparse()

    def set_current(self, value: str) -> None:
        if len(self.args) > 0:
            self.args[-1] = value
        else:
            self.command = value

    def get_current(self) -> str:
        return self.args[- 1] if len(self.args) > 0 else self.command

    current = property(get_current, set_current)

    def __parse(self):
        self.args = self.text.split(' ')

    def __deparse(self):
        self.text = ' '.join(self.args)
