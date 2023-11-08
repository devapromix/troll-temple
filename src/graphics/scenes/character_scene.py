import tcod as T
from common.utils import *

class CharacterScene:
    def __init__(self, turns, player):
        self.turns = turns
        self.player = player

    def show(self):
        from common.game import clear, out_file, refresh, out, anykey, COLOR_TITLE, draw_statistics
        from mobs.player import GAME_CLASSES
        from common.calendar import Calendar
        calendar = Calendar()
        clear()

        self.game_class = GAME_CLASSES[self.player.game_class.value - 1]
        out(2, 1, self.player.name, COLOR_TITLE)

        out(2, 3, "Race         " + "Human", T.light_grey)
        out(2, 4, "Class        " + self.game_class[0], T.light_grey)
        out(2, 6, "Level        " + str(self.player.level), T.light_grey)
        out(2, 7, "Experience   " + str(self.player.exp) + "/" + str(self.player.max_exp()), T.light_grey)
        if self.player.life_regen > 0:
            regen = " (+" + str(self.player.life_regen) + ")"
        else:
            regen = ""
        out(2, 9, "Life         " + self.player.life.to_string() + regen, T.light_grey)
        if self.player.mana_regen > 0:
            regen = " (+" + str(self.player.mana_regen) + ")"
        else:
            regen = ""
        out(2, 10, "Mana         " + self.player.mana.to_string() + regen, T.light_grey)
        r = ''
        if self.player.range > 1:
            r = ' ranged'
        out(2, 12, "Damage       " + describe_dice(*self.player.dice) + " (" + str_dice(*self.player.dice) + ")" + r,T.light_grey)
        out(2, 13, "Armor        " + str(self.player.armor), T.light_grey)
        out(2, 15, "Speed        " + str(self.player.speed), T.light_grey)
        out(2, 16, "Magic power  " + str(self.player.magic), T.light_grey)
        out(2, 17, "Light radius " + str(self.player.fov_range + self.player.radius), T.light_grey)
        out(2, 18, "Range        " + str(self.player.range), T.light_grey)
        out(2, 19, "", T.light_grey)
        out(2, 20, "", T.light_grey)
        out(2, 21, "", T.light_grey)
        out(2, 22, "", T.light_grey)

        out(40, 3, calendar.get_time_date(self.turns), T.light_grey)
        draw_statistics(5)

        out(0, 28, "Press [ENTER] to continue...", T.light_grey)
        refresh()
        anykey()












