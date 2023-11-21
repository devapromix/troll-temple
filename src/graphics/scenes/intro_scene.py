from .single_page_scene import SinglePageScene
from graphics.color import Color

class IntroScene(SinglePageScene):
    def _draw_content(self) -> None:
        from graphics.window import out_file, out
        out(0, 2, "Many centuries ago...", Color.TITLE.value)
        out_file(10, 4, '../assets/texts/help.txt', Color.ITEM.value)

