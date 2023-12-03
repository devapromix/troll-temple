from .Item import *

class LightSource(Item):
    ABSTRACT = True
    slot = 'l'

    @property
    def descr(self):
        if self.turns_left == self.turns:
            s = self.name
        else:
            p = 100 * self.turns_left // self.turns
            s = '%s (%s%%)' % (self.name, p)
        return s + self.mod_descr

    def __init__(self):
        super(LightSource, self).__init__()
        self.turns_left = self.turns

    def on_equip(self, player):
        player.change_light_range(self.light_range)
        player.visibility()
        return True

    def on_unequip(self, player):
        player.change_light_range(-self.light_range)


class Torch(LightSource):
    name = 'torch'
    art = 'torch'
    glyph = '|', T.dark_orange
    dungeons = 1, 11
    turns = 150
    light_range = 6


class CopperLamp(LightSource):
    name = 'copper lamp'
    art = 'lamp'
    glyph = 'o', T.yellow
    dungeons = 4, 10
    rarity = 5
    turns = 300
    light_range = 8


class BronzeLamp(LightSource):
    name = 'bronze lamp'
    art = 'lamp'
    glyph = 'o', T.light_yellow
    dungeons = 6, 11
    rarity = 10
    turns = 450
    light_range = 9

class SilverLamp(LightSource):
    name = 'silver lamp'
    art = 'lamp'
    glyph = 'o', T.lighter_yellow
    dungeons = 8, 12
    rarity = 15
    turns = 600
    light_range = 10





























