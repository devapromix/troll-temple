from common.utils import rand, describe_dice
from .item import Item


class Weapon(Item):
    ABSTRACT = True
    slot = 'w'
    common = 7

    def __init__(self):
        super(Weapon, self).__init__()
        if rand(1, 5) == 1:
            a, b, c = self.dice
            c += rand(1, 3)
            if rand(1, 9) == 1:
                b += rand(1, 2)
            self.dice = a, b, c

    @property
    def descr(self):
        return '%s (%s)%s' % (self.name, describe_dice(*self.dice), self.mod_descr)


class EliteWeapon(Weapon):
    ABSTRACT = True
    rarity = 10


class UniqueWeapon(Weapon):
    ABSTRACT = True
    rarity = 15