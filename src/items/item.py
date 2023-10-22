from common.game import UNKNOWN_GLYPH, message
from common.utils import Register


class Item(object, metaclass=Register):
    ALL = []
    ABSTRACT = True
    common = 10

    glyph = UNKNOWN_GLYPH
    dungeons = 0, 0
    slot = None
    speed = 0
    armor = 0
    rarity = 1
    plural = False

    @property
    def descr(self):
        return self.name + self.mod_descr

    @property
    def a(self):
        if self.plural:
            return self.descr
        else:
            d = self.descr
            if d[0].lower() in 'aeiuo':
                return 'an ' + self.descr
            else:
                return 'a ' + self.descr

    @property
    def mod_descr(self):
        s = ''
        if self.speed != 0:
            s += ' (%s%d speed)' % ('+' if self.speed > 0 else '', self.speed)
        if self.armor != 0:
            s += ' (%s%d armor)' % ('+' if self.armor > 0 else '', self.armor)
        return s

    def on_equip(self, player):
        player.speed += self.speed
        player.armor += self.armor

    def on_unequip(self, player):
        player.speed -= self.speed
        player.armor -= self.armor

    def on_use(self, player):
        message('You don\'t know how to use %s.' % self.descr)