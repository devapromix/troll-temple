import tcod as T
from .single_page_scene import SinglePageScene
from graphics.color import Color

class TitleScene(SinglePageScene):
    def _draw_content(self) -> None:
        from common.constants import VERSION
        from graphics.window import out_file, out
        out_file(5, 4, '../assets/texts/troll.txt', T.green)
        out_file(45, 4, '../assets/texts/lonely_mountain.txt', T.darker_yellow)
        out_file(10, 10, '../assets/texts/temple.txt', T.light_red)
        out(35, 17, ' v.' + VERSION, T.light_green)
        out(6, 22, 'by Apromix and Gandifil', T.light_yellow)
        out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)

