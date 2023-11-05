from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import AddMaxHp
from common.modifiers.mod import Mod
from .perk import *


class Vitality(Perk):
    __name = 'Defence Art2'
    __descr = "Increase your life"
    modifier = AddMaxHp(20)
    max_count = 10


class DefenceArt(Perk):
    __name = 'Defence Art'
    __descr = "Increase common abilities to evade and to supress damage"
    modifier = AggregateModifier(
        Mod('armor', 5),
        Mod('evasion', 10),
        AddMaxHp(10)
    )
    max_count = 5


class Agility(Perk):
    __descr = "Increase speed, accuracy and evasion"
    modifier = AggregateModifier(
        Mod('speed', 1),
        Mod('accuracy', 50),
        Mod('evasion', 5)
    )
    rarity = PerkRarity.RARE