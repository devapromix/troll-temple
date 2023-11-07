import tcod as T

class FinalScene:
    def __init__(self, player):
        self.player = player

    def show(self):
        from common.game import clear, out_file, refresh, out, anykey, Quit, COLOR_TITLE
        clear()
        out(0, 2, "The end...", COLOR_TITLE)
        out_file(10, 4, '../assets/texts/final.txt', T.lighter_grey)
        out(0, 28, "Press [ENTER] to exit...", T.light_grey)
        refresh()
        anykey()
        raise Quit()
        