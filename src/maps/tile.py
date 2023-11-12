import tcod as T

class Tile(object):
    walkable = True
    transparent = True
    glyph = '?', T.red
    known_glyph = ' ', T.white

    def __init__(self):
        self.mob = None
        self.obj = None
        self.items = []

    @property
    def visible_glyph(self):
        from common.game import GAME
        from mobs.player import Invisibility
        player = GAME.player
        if self.mob and not (self.mob == player and player.invisibility == Invisibility.FULL):
            if self.mob == player and player.invisibility == Invisibility.SHADOW:
                return self.mob.glyph[0], T.darkest_grey
            if self.mob.poisoned > 0:
                return self.mob.glyph[0], T.lighter_green
            elif self.mob.confused:
                return self.mob.glyph[0], T.lightest_blue
            else:
                return self.mob.glyph
        elif self.items:
            return self.items[-1].glyph
        elif self.obj:
            if self.obj.used:
                return self.obj.glyph[0], T.grey
            else:
                return self.obj.glyph
        else:
            return self.glyph

    def remember_glyph(self):
        if self.items:
            self.known_glyph = self.items[-1].glyph
        else:
            self.known_glyph = self.glyph

    def on_enter(self):
        pass





















