import tcod as T

class IntroScene:
    def show(self):
        from common.game import clear, out_file, refresh, out, anykey, COLOR_TITLE
        clear()
        out(0, 2, "Many centuries ago...", COLOR_TITLE)
        out_file(10, 4, '../assets/texts/help.txt', T.lighter_grey)
        out(0, 28, "Press [ENTER] to continue...", T.light_grey)
        refresh()
        anykey()

