import tcod as T
from .single_page_scene import SinglePageScene
from graphics.color import Color

class InfoScene(SinglePageScene):

    def message(self, title, msg):
        self.title = title
        self.msg = msg

    def _draw_content(self) -> None:
        from common.game import out_file, out, out_file, out_text
        out_file(35, 5, '../assets/texts/lonely_mountain.txt', T.darker_yellow)
        out(0, 2, self.title, Color.TITLE.value)
        out_text(10, 5, 40, self.msg, Color.ITEM.value)
        out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)