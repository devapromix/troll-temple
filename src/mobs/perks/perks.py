from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import AddMaxLife
from common.modifiers.mod import Mod
from .perk import *


class Powerful(Perk):
    __name = 'powerful'
    __descr = "Increase your life"
    modifier = AddMaxLife(5)
    max_count = 10


class DefenceArt(Perk):
    __name = 'defence art'
    __descr = "Increase common abilities to evade and to supress damage"
    modifier = AggregateModifier(
        Mod('armor', 5),
        Mod('evasion', 10),
        AddMaxLife(10)
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


class Hero(Perk):
    __descr = "You feel how Gods like your actions. All things in world help you. All base attributes increased"
    modifier = AggregateModifier(
        Mod('speed', 1),
        Mod('accuracy', 50),
        Mod('evasion', 10),
        Mod('armor', 5),
        AddMaxLife(20),
    )
    max_count = 1
    rarity = PerkRarity.LEGEND

class Indomitable(Perk):
    __name = "indomitable"
    __descr = "Increase damage"
    #modifier = AddDamage(1)
    max_count = 5

class Stoneheart(Perk):
    __name = "stoneheart"
    __descr = "Increase armor"
    modifier = Mod('armor', 2)
    max_count = 10

class EagleEye(Perk): # only class ranger
    __name = "eagle eye"
    __descr = "Improves the viewing radius"
    modifier = Mod('radius', 1)
    max_count = 2

class Poisoner(Perk): # only class thief
    __name = "poisoner"
    __descr = "Poisons enemies more effective"
    modifier = Mod('poison', 1)
    max_count = 3
    rarity = PerkRarity.RARE

class Bower(Perk): # only class thief
    name = "bower"
    descr = "You can use a bow."
    #self.can_use_bow = True
    max_count = 1
    rarity = PerkRarity.LEGEND



