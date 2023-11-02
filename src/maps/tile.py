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
        if self.mob:
            if self.mob.poisoned > 0:
                return self.mob.glyph[0], T.lighter_green
            elif self.mob.confused:
                return self.mob.glyph[0], T.lightest_blue
            else:
                return self.mob.glyph
        elif self.items:
            return self.items[-1].glyph
        elif self.obj:
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





















