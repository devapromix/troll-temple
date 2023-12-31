import tcod as T
from common.game import message
from common.utils import Register
from common.game import COLOR_ITEM


class Item(object, metaclass=Register):
    ALL = []
    ABSTRACT = True
    common = 10
    name = "unknown item"
    description = ''
    art = 'unknown_item'
    max_amount = 1
    amount = 1

    glyph = "?", T.red
    color = COLOR_ITEM
    dungeons = 0, 0
    slot = None
    rarity = 1
    plural = False

    @property
    def descr(self):
        return self.name + self.mod_descr + self.mod_amount

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

    @property
    def mod_amount(self):
        ret = ""
        if self.max_amount > 1:
            ret = " %sx" % str(self.amount)
        return ret

    def on_equip(self, player):
        return True

    def on_unequip(self, player):
        pass

    def on_use(self, player):
        message('You don\'t know how to use %s.' % self.descr)
        