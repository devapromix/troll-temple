from copy import copy

from common.modifiers.modifier import Modifier
from common.utils import rand
from mobs.damage import Damage


class Reflection(Modifier):
    def __init__(self, chance_percent: int, value_percent: int):
        self.chance_percent = chance_percent
        self.value_percent = value_percent
        self.f = lambda damage: self.__mod_damaged(damage)

    @property
    def descr(self):
        return "Reflects %d damage with chance %d" % (self.value_percent, self.chance_percent)

    def commit(self, mob):
        super().commit(mob)
        mob.on_damage += self.f

    def rollback(self, mob):
        super().rollback(mob)
        mob.on_damage -= self.f

    def __mod_damaged(self, damage: Damage):
        if rand(0, 99) < self.chance_percent:
            reflected_damage = copy(damage)
            damage.attacker.damage(reflected_damage, damage.defender)
