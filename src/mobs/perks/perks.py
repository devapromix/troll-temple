from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import *
from common.modifiers.add_damage import *
from common.modifiers.fight_for_life import FightForLife
from common.modifiers.mod import Mod
from common.modifiers.reflection import Reflection
from .perk import *
from ..player import Classes


class Powerful(Perk):
    _name = 'powerful'
    _descr = "Increase your life"
    modifier = AddMaxLife(5)
    max_count = 10


class DefenceArt(Perk):
    _name = 'defence art'
    _descr = "Increase common abilities to evade and to supress Damage"
    modifier = AggregateModifier(
        Mod('armor', 5),
        Mod('evasion', 10),
        AddMaxLife(10)
    )
    max_count = 5


class Agility(Perk):
    _descr = "Increase speed, accuracy and evasion"
    modifier = AggregateModifier(
        Mod('speed', 1),
        Mod('accuracy', 50),
        Mod('evasion', 5)
    )
    rarity = PerkRarity.RARE


class ContrImpulse(Perk):
    _descr = "Let you reflect a small portion of incoming damage back to the attacker with low chance"
    modifier = AggregateModifier(
        Reflection(20, 20)
    )
    max_count = 2
    classes = {Classes.FIGHTER}


class ParryMaster(LegendPerk):
    _descr = ("Become a master of the blade. This advanced skill allows you to deflect incoming attacks with precise "
              "timing, turning the tables on your adversaries. Parry Master not only reduces incoming damage but also "
              "increase portions of it, which reflect back to the attacker. Your exceptional parrying skills can punish"
              " those who dare to challenge you")
    modifier = AggregateModifier(
        Reflection(50, 50),
        Mod('armor', 15),
        Mod('blocking', 15),
    )
    classes = {Classes.FIGHTER}


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


class IroncladDefender(LegendPerk):
    _descr = ("The Ironclad Defender perk transforms you into an unyielding fortress on the battlefield. "
              "With unwavering determination, you prioritize defense above all else, "
              "bolstering your resistance to Damage. However, this unwavering focus on defense comes at the cost of agility and evasion")
    modifier = AggregateModifier(
        AddMaxLife(100),
        Mod('armor', 25),
        Mod('evasion', -100),
        Mod('speed', -1),
    )
    classes = {Classes.FIGHTER}

class EagleEye(Perk):
    _name = "eagle eye"
    _descr = "The eagle eye allows you to increase the distance from which you can shoot at a target"
    modifier = Mod('radius', 1)
    max_count = 2
    classes = {Classes.RANGER}

class Poisoner(Perk):
    _name = "poisoner"
    _descr = "You discover new alchemy poisons and poison your enemies more effectively"
    modifier = Mod('poison', 1)
    max_count = 3
    rarity = PerkRarity.RARE
    classes = {Classes.THIEF}

class Bower(LegendPerk):
    _name = "bower"
    _descr = "You can use a bow and hit your enemies with it"
    #self.can_use_bow = True
    classes = {Classes.THIEF}

class InnerReserves(Perk):
    _name = 'Inner Reserves'
    _descr = "Increase your mana and life"
    modifier = AggregateModifier(
        AddMaxLife(2),
        AddMaxMana(7)
    )
    max_count = 10
    classes = {Classes.MAGE}



