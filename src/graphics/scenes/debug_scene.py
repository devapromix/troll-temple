from abc import abstractmethod
from typing import List

import pygame

from common.utils import Register
from graphics.layout import Layout
from graphics.point import Point
from graphics.scenes.scene import Scene
import tcod as T


class DebugCommand(metaclass=Register):
    ALL = []
    ABSTRACT = True
    args_count = 0

    @abstractmethod
    def run(self, **kwargs):
        pass

    @abstractmethod
    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        pass


class GetCommand(DebugCommand):
    args_count = 1

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
        if index == 0:
            return [cls.__name__ for cls in items.Item.Item.ALL if value.lower() in cls.__name__.lower()]
        else:
            return []


class SpawnCommand(DebugCommand):
    args_count = 1

    def run(self, *args):
        name = args[0]

        from mobs.monster import Monster
        for cls in Monster.ALL:
            if cls.__name__.lower() == name.lower():
                from common.game import GAME
                GAME.map.place_monsters(cls)

    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        from mobs.monster import Monster
        if index == 0:
            return [cls.__name__ for cls in Monster.ALL if value.lower() in cls.__name__.lower()]
        else:
            return []


class LevelUpCommand(DebugCommand):
    def run(self, *args):
        from common.game import GAME
        GAME.player.advance()

    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        return []


class AscendCommand(DebugCommand):
    def run(self, *args):
        from common.game import GAME
        GAME.ascend()

    def auto_complete_arg(self, value: str, index: int) -> List[str]:
        return []


class DebugScene(Scene):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.__args = []
        self.__args_complete = []
        self.__selected_index = None
        self.__parse()

    def _draw_content(self) -> None:
        auto_complete_list=[]
        line = Layout(Point(1, 0))
        for i, arg in enumerate(self.__args):
            auto_complete_list = self.__args_complete[i]
            lower_auto_complete_list = [x.lower() for x in auto_complete_list]
            line.print(arg, T.lighter_green if arg.lower() in lower_auto_complete_list else T.lighter_red)
            if i < len(self.__args)-1:
                line.print(' ')
        line.print('_')

        if len(auto_complete_list) > 0:
            line.offset = len(' '.join(self.__args[:-1]))
            line.offset = line.offset + 1 if line.offset > 0 else 0
            line.color = T.lighter_blue
            line.next()
            for i, text in enumerate(auto_complete_list):
                line.print_line(text, background_color=T.darker_grey if i == self.__selected_index else None)

        from common.game import out_file
        out_file(50, 0, '../assets/texts/debug_help.txt', T.white)

    def _check_input(self, key: int) -> bool:
        if key == pygame.K_RETURN:
            self.__run()
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
        if key == pygame.K_UP:
            self.__selected_index = self.__selected_index - 1 \
                if self.__selected_index != 0 else len(self.__args_complete[-1]) - 1
            return True
        if key == pygame.K_DOWN:
            self.__selected_index = self.__selected_index + 1 \
                if self.__selected_index != len(self.__args_complete[-1]) - 1 else 0
            return True


        name = pygame.key.name(key)
        if len(name) == 1:
            self.text += name
            self.__parse()
            return True
        return False

    def __run(self):
        command = self.__current_command
        if command is not None:
            self.__current_command.run(*self.__args[1:])
        self.exit()

    @property
    def __current_command(self) -> DebugCommand:
        for cls in DebugCommand.ALL:
            if cls.__name__.lower() == self.__args[0].lower() + "command":
                return cls()

    def __auto_complete_list(self, index: int) -> List[str]:
        if index > 0:
            index1 = len(self.__args) - 1
            command = self.__current_command
            names = command.auto_complete_arg(self.__args[index1], index1 - 1) if command is not None else []
            return [x for x in names if self.__args[index1].lower() in x.lower()]
        else:
            names1 = map(lambda x: x.__name__[:-len("command")], DebugCommand.ALL)
            return [x1 for x1 in names1 if self.__args[0].lower() in x1.lower()]

    def __complete(self) -> None:
        auto_complete_list = self.__args_complete[-1]
        if len(auto_complete_list) > 0:
            self.__args[-1] = auto_complete_list[self.__selected_index]
            self.__deparse()
            command = self.__current_command
            if command is not None and len(self.__args) == command.args_count + 1:
                self.__run()

    def __parse(self):
        self.__args = self.text.split(' ')
        self.__args_complete = [self.__auto_complete_list(i) for i in range(len(self.__args))]
        self.__selected_index = 0

    def __deparse(self):
        self.text = ' '.join(self.__args)
