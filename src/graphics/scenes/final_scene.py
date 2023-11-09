from graphics.color import Color

class FinalScene:
    def __init__(self, player):
        self.player = player

    def show(self):
        from common.game import clear, out_file, refresh, out, anykey, Quit
        clear()
        out(0, 2, "The end...", Color.TITLE.value)
        out_file(10, 4, '../assets/texts/final.txt', Color.ITEM.value)
        out(0, 28, "Press [ENTER] to exit...", Color.ITEM.value)
        refresh()
        anykey()
        raise Quit()
        