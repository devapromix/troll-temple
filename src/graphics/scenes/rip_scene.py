import tcod as T
from .single_page_scene import SinglePageScene
from graphics.color import Color

class RipScene(SinglePageScene):
    def __init__(self, turns, player):
        super().__init__()
        self.turns = turns
        self.player = player

    def _draw_content(self) -> None:
        from common.game import out_file, out, anykey, COLOR_TITLE, draw_statistics
        from common.calendar import Calendar
        calendar = Calendar()

        out(0, 2, "Rest in peace...", Color.TITLE.value)
        out_file(10, 8, '../assets/texts/rip.txt', Color.ITEM.value)

        out(12, 10, 'REST', T.grey, T.black, 14)
        out(12, 11, 'IN', T.grey, T.black, 14)
        out(12, 12, 'PEACE', T.grey, T.black, 14)

        out(12, 15, self.player.name, T.yellow, T.black, 14)
        out(12, 16, 'killed by a', T.grey, T.black, 14)
        out(12, 17, 'fire goblin', T.grey, T.black, 14)

        day, year = calendar.get_day(self.turns)

        out(12, 20, calendar.get_month_name(day) + ' ' + str(calendar.get_month_num(day) + 1), Color.ITEM.value, T.black, 14)
        out(12, 21, str(year), T.grey, T.black, 14)

        out(4, 23, '___)/\/\/\/\/\/\/\/\/\/\/\(___', T.green)

        out(40, 6, 'Epitaph', Color.TITLE.value)
        out_file(40, 8, '../assets/texts/epitaph.txt', Color.ITEM.value)

        out(40, 13, 'You were killed by a fire goblin on level 1', Color.ITEM.value)
        out(40, 14, 'of the Old Temple.', Color.ITEM.value)

        draw_statistics(16)

        out(0, 28, "Press [ENTER] to exit...", Color.ITEM.value)

    def _check_input(self, key: int) -> bool:
        from common.game import Quit
        super()._check_input(key)
        raise Quit()