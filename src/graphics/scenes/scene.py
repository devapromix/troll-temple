from graphics.window import Window


class Scene:
    def __init__(self):
        self.has_footer = True
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
        window = Window.instance()
        window.clear()
        self._draw_content()
        if self.has_footer:
            from graphics.color import Color
            window.out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)
        window.refresh()

    def _draw_content(self) -> None:
        raise NotImplementedError()

    def _check_input(self, key: int) -> bool:
        """
        Process input's keys from user.

        :return: True if key was caught.
        """

        raise NotImplementedError()

    ''' Stop showing of this scene'''
    def exit(self):
        self.__is_exit = True