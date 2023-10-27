from common.game import COLOR_MAGIC
from common.utils import rand
from .Item import Item

class Equipment(Item):
    ABSTRACT = True
    magical = False
    speed = 0
    
    def suffix(self, suffix_name):
        if not self.magical:
            self.name += " of " + suffix_name
            self.color = COLOR_MAGIC
            self.magical = True
            return True
        else:
            return False

    def on_equip(self, player):
        player.speed += self.speed
        return True

    def on_unequip(self, player):
        player.speed -= self.speed

    @property
    def mod_descr(self):
        s = ''
        if self.speed != 0:
            s += ' %s%d speed' % ('+' if self.speed > 0 else '', self.speed)
        return s.strip()
