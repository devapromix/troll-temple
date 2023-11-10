

class Scene:
    def __init__(self):
        self.__is_exit = False

    def show(self) -> None:
        from common.game import readkey
        while True:
            self.__draw()
            while not self._check_input(readkey()):
                pass
            if self.__is_exit:
                return

    def __draw(self) -> None:
        from common.game import clear, refresh
        clear()
        self._draw_content()
        refresh()

    def _draw_content(self) -> None:
        raise NotImplementedError()

    ''' Process input's keys from user. Return True if key was caught.'''
    def _check_input(self, key: int) -> bool:
        raise NotImplementedError()

    ''' Stop showing of this scene'''
    def exit(self):
        self.__is_exit = True