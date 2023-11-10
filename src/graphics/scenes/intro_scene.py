from graphics.color import Color

class IntroScene:
    def show(self):
        from common.game import clear, out_file, refresh, out, anykey
        clear()
        out(0, 2, "Many centuries ago...", Color.TITLE.value)
        out_file(10, 4, '../assets/texts/help.txt', Color.ITEM.value)
        out(0, 28, "Press [ENTER] to continue...", Color.ITEM.value)
        refresh()
        anykey()

