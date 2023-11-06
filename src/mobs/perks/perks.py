from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import AddMaxLife
from common.modifiers.fight_for_life import FightForLife
from common.modifiers.mod import Mod
from .perk import *
from ..player import Classes


class Powerful(Perk):
    __name = 'powerful'
    __descr = "Increase your life"
    modifier = AddMaxLife(5)
    max_count = 10


class DefenceArt(Perk):
    __name = 'defence art'
    __descr = "Increase common abilities to evade and to supress Damage"
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


class FightForLife(Perk):
    __descr = "Powerful wish to live"
    modifier = AggregateModifier(
        FightForLife(),
    )
    max_count = 1
    rarity = PerkRarity.LEGEND

class Indomitable(Perk):
    __name = "indomitable"
    __descr = "Increase Damage"
    #modifier = AddDamage(1)
    max_count = 5

class Stoneheart(Perk):
    __name = "stoneheart"
    __descr = "Increase armor"
    modifier = Mod('armor', 2)
    max_count = 10


class IroncladDefender(Perk):
    __descr = "The Ironclad Defender perk transforms you into an unyielding fortress on the battlefield. With unwavering determination, you prioritize defense above all else, bolstering your resistance to Damage. However, this unwavering focus on defense comes at the cost of agility and evasion"
    modifier = AggregateModifier(
        AddMaxLife(100),
        Mod('armor', 25),
        Mod('evasion', -100),
        Mod('speed', -1),
    )
    max_count = 1
    rarity = PerkRarity.LEGEND
    classes = {Classes.FIGHTER}

class EagleEye(Perk): # only class Classes.RANGER
    __name = "eagle eye"
    __descr = "Improves the viewing radius"
    modifier = Mod('radius', 1)
    max_count = 2
    classes = {Classes.THIEF}

class Poisoner(Perk): # only class Classes.THIEF
    __name = "poisoner"
    __descr = "Poisons enemies more effective"
    modifier = Mod('poison', 1)
    max_count = 3
    rarity = PerkRarity.RARE
    classes = {Classes.THIEF}

class Bower(Perk): # only class Classes.THIEF
    name = "bower"
    descr = "You can use a bow."
    #self.can_use_bow = True
    max_count = 1
    rarity = PerkRarity.LEGEND
    classes = {Classes.THIEF}



