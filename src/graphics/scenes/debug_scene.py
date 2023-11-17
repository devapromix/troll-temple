from abc import abstractmethod
from typing import List

import pygame

from common.utils import Register
from graphics.line import Line
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
        self.command = ""
        self.args = []
        self.has_space = False

    def _draw_content(self) -> None:
        from common.game import out, out_list

        line = Line(1, 0)
        auto_complete_list = self.__auto_complete_list_command
        lower_auto_complete_list = [x.lower() for x in auto_complete_list]
        line.print(self.command, T.lighter_green if self.command.lower() in lower_auto_complete_list else T.lighter_red)
        for i, arg in enumerate(self.args):
            line.print(' ')
            auto_complete_list = self.__auto_complete_list_arg(i)
            lower_auto_complete_list = [x.lower() for x in auto_complete_list]
            line.print(arg, T.lighter_blue if arg.lower() in lower_auto_complete_list else T.lighter_red)
        if self.has_space:
            line.print(' ')
        line.print('_')

        auto_complete_list = self.__auto_complete_list
        if len(auto_complete_list) > 0:
            out(1, 1, auto_complete_list[0], T.lighter_blue, T.darker_grey)
            out_list(1, 2, auto_complete_list[1:], T.lighter_blue)

        from common.game import out_file
        out_file(50, 0, '../assets/texts/debug_help.txt', T.white)

    def _check_input(self, key: int) -> bool:
        if key == pygame.K_RETURN:
            command = self.__current_command
            if command is not None:
                self.__current_command.run(*self.args)
            self.exit()
            return True
        if key == pygame.K_SPACE:
            if not self.has_space:
                self.has_space = True
                return True
        if key == pygame.K_BACKSPACE:
            if self.has_space:
                self.has_space = False
            elif len(self.current) > 0:
                self.current = self.current[:-1]
            elif len(self.args) > 0:
                self.args.pop(len(self.args) - 1)
                self.has_space = True
            return True
        if key == pygame.K_TAB:
            self.__complete()
            return True

        name = pygame.key.name(key)
        if len(name) == 1:
            if self.has_space:
                self.args.append(name)
                self.has_space = False
            else:
                self.current = self.current + name
            return True
        return False

    @property
    def __current_command(self) -> DebugCommand:
        for cls in DebugCommand.ALL:
            if cls.__name__.lower() == self.command.lower() + "command":
                return cls()
        # return None

    @property
    def __auto_complete_list(self) -> List[str]:
        if len(self.args) > 0:
            return self.__auto_complete_list_arg(len(self.args) - 1)
        else:
            return self.__auto_complete_list_command

    @property
    def __auto_complete_list_command(self) -> List[str]:
        names = map(lambda x: x.__name__[:-len("command")], DebugCommand.ALL)
        return [x for x in names if self.command.lower() in x.lower()]

    def __auto_complete_list_arg(self, index: int) -> List[str]:
        command = self.__current_command
        names = command.auto_complete_arg(self.args[index], index) if command is not None else []
        return [x for x in names if self.args[index].lower() in x.lower()]

    def __complete(self) -> None:
        auto_complete_list = self.__auto_complete_list
        if len(auto_complete_list) > 0:
            self.current = auto_complete_list[0]

    def set_current(self, value: str) -> None:
        if len(self.args) > 0:
            self.args[-1] = value
        else:
            self.command = value

    def get_current(self) -> str:
        return self.args[- 1] if len(self.args) > 0 else self.command

    current = property(get_current, set_current)
