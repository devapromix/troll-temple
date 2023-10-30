from common.game import UNKNOWN_GLYPH, message
from common.utils import Register
from common.game import COLOR_ITEM


class Item(object, metaclass=Register):
    ALL = []
    ABSTRACT = True
    common = 10

    glyph = UNKNOWN_GLYPH
    color = COLOR_ITEM
    dungeons = 0, 0
    slot = None
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
        return ""

    def on_equip(self, player):
        return True

    def on_unequip(self, player):
        pass

    def on_use(self, player):
        message('You don\'t know how to use %s.' % self.descr)
        