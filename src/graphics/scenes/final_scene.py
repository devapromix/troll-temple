import tcod as T
from .single_page_scene import SinglePageScene
from graphics.color import Color

class FinalScene(SinglePageScene):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def show(self):
        from common.game import out_file, out
        out(0, 2, "The end...", Color.TITLE.value)
        out_file(10, 4, '../assets/texts/final.txt', Color.ITEM.value)
        out(0, 28, "Press [ENTER] to exit...", Color.ITEM.value)

    def _check_input(self, key: int) -> bool:
        from common.game import Quit
        super()._check_input(key)
        raise Quit()        