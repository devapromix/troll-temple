class Scene:
    def show(self) -> None:
        from common.game import readkey
        while True:
            self.__draw()
            if self._check_input(readkey()):
                return

    def __draw(self) -> None:
        from common.game import clear, refresh
        clear()
        self._draw_content()
        refresh()

    def _draw_content(self) -> None:
        raise NotImplementedError()

    def _check_input(self, key: int) -> bool:
        raise NotImplementedError()
