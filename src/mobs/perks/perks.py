from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import *
from common.modifiers.add_damage import *
from common.modifiers.fight_for_life import FightForLife
from common.modifiers.mod import Mod
from .perk import *
from ..player import Classes


class Powerful(Perk):
    _name = 'powerful'
    _descr = "Increase your life"
    modifier = AddMaxLife(5)
    max_count = 10


class DefenceArt(Perk):
    _name = 'defence art'
    _descr = "Increase common abilities to evade and to supress damage."
    modifier = AggregateModifier(
        Mod('armor', 5),
        Mod('evasion', 10),
        AddMaxLife(10)
    )
    max_count = 5


class Agility(RarePerk):
    _descr = "Increase speed, accuracy and evasion"
    modifier = AggregateModifier(
        Mod('speed', 1),
        Mod('accuracy', 50),
        Mod('evasion', 5)
    )
    max_count = 1


class Hero(LegendPerk):
    _descr = "You feel how Gods like your actions. All things in world help you. All base attributes increased"
    modifier = AggregateModifier(
        Mod('speed', 1),
        Mod('accuracy', 50),
        Mod('evasion', 10),
        Mod('armor', 5),
        AddMaxLife(20),
    )


class FightForLife(LegendPerk):
    _descr = "Powerful wish to live"
    modifier = AggregateModifier(
        FightForLife(),
    )


class Indomitable(Perk):
    _name = "indomitable"
    _descr = "Increase damage"
    modifier = DamageMod(1)
    max_count = 5


class Stoneheart(Perk):
    _name = "stoneheart"
    _descr = "Increase armor"
    modifier = Mod('armor', 2)
    max_count = 10


class InnerReserves(Perk):
    _name = 'inner reserves'
    _descr = "Increase your mana and life"
    modifier = AggregateModifier(
        AddMaxLife(2),
        AddMaxMana(7)
    )
    max_count = 10
    classes = {Classes.MAGE}



