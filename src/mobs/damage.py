from enum import Enum

from common.utils import rand, roll


class DamageStatus(Enum):
    NORMAL = 0,
    CRITICAL = 1,
    EVADED = 2,
    BLOCKED = 3,
    ABSORBED = 4,


def check_evasion(attacker, defender):
    accuracy = max(attacker.accuracy, 1)
    evasion = max(defender.evasion, 1)

    # Mob have at least ~5% (1/20) chance to evade strike and to success strike
    accuracy = accuracy if accuracy > evasion//20 else evasion//20
    evasion = evasion if evasion > accuracy//20 else accuracy//20
    return rand(1, evasion + accuracy) <= evasion


class Damage:
    def __init__(self, status, value):
        self.status = status
        self.value = value

    def __int__(self):
        return self.value

    @staticmethod
    def normal(value):
        return Damage(DamageStatus.NORMAL, value)

    @staticmethod
    def crit(value):
        return Damage(DamageStatus.CRITICAL, value)

    @staticmethod
    def evaded():
        return Damage(DamageStatus.EVADED, 0)

    @staticmethod
    def blocked():
        return Damage(DamageStatus.BLOCKED, 0)

    @staticmethod
    def absorbed():
        return Damage(DamageStatus.ABSORBED, 0)

    @staticmethod
    def calculate(attacker, defender):
        if check_evasion(attacker, defender):
            return Damage.evaded()

        dmg = roll(*attacker.dice) + attacker.damage_bonus
        dmg = defender.calc_damage(dmg)
        if dmg > 0:
            if defender.blocking > 0 and rand(1, 100 - defender.blocking) == 1:
                return Damage.blocked()
            if rand(1, 20) == 1:
                return Damage.crit(dmg * 2)
            else:
                return Damage.normal(dmg)
        else:
            return Damage.absorbed()