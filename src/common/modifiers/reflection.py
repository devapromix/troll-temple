from copy import copy

from common.game import message
from common.utils import rand
from mobs.damage import *
from .modifier import Modifier
from .tag_mod import Tag


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
        if damage.value > 0:
            chance_percent = self.chance_percent + damage.defender.reflect_chance_bonus
            if ((Tag.BlockedAlwaysReflect in damage.defender.tags and damage.status == DamageStatus.BLOCKED)
                    or rand(0, 99) < chance_percent):
                reflected_damage = copy(damage)
                reflected_damage.attacker, reflected_damage.defender = damage.defender, damage.attacker
                value_percent = self.value_percent + damage.defender.reflect_damage_bonus
                reflected_damage.value = damage.raw_value * value_percent // 100
                damage.attacker.damage(reflected_damage)
                from mobs.player import Player
                if type(damage.defender) == Player:
                    message("You return damage back!")
