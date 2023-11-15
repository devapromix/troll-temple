from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import *
from common.modifiers.mod import Mod
from common.modifiers.reflection import Reflection
from .perk import *
from ..player import Classes


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
