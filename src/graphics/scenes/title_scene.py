import tcod as T
from graphics.color import Color

class TitleScene:
    def show(self):
        from common.game import VERSION, clear, out_file, out, refresh, anykey
        clear()
        out_file(5, 4, '../assets/texts/troll.txt', T.green)
        out_file(45, 4, '../assets/texts/lonely_mountain.txt', T.darker_yellow)
        out_file(10, 10, '../assets/texts/temple.txt', T.light_red)
        out(35, 17, ' v.' + VERSION, T.light_green)
        out(6, 22, 'by Apromix and Gandifil', T.light_yellow)
        out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)
        refresh()
        anykey()

