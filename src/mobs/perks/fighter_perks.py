from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import *
from common.modifiers.mod import Mod
from common.modifiers.reflection import Reflection
from common.modifiers.tag_mod import TagMod, Tag
from .perk import *
from ..player import Classes


class ContrImpulse(Perk):
    _descr = "Let you reflect a small portion of incoming damage back to the attacker with low chance"
    modifier = AggregateModifier(
        Reflection(20, 20)
    )
    max_count = 2
    classes = {Classes.FIGHTER}


class ReflectiveMastery(Perk):
    _descr = ("Unleash the full potential of reflection with the Reflective Mastery perk. This advanced skill not only "
              "enhances your ability to deflect incoming attacks but also maximizes the power of the reflected damage. "
              "As you delve deeper into the art of redirection, Reflective Mastery transforms you into a formidable "
              "force on the battlefield, punishing adversaries with their own aggression.")
    modifier = AggregateModifier(
        Mod('reflect_damage_bonus', 10),
        Mod('reflect_chance_bonus', 5),
    )
    max_count = 2
    classes = {Classes.FIGHTER}


class DefiantRiposte(RarePerk):
    _descr = ("Elevate your defensive capabilities to new heights with the Defiant Riposte perk. This exceptional "
              "skill ensures that every successful block transforms into a guaranteed reflection of damage back to "
              "your assailant. No longer subject to chance, Defiant Riposte empowers you to confidently engage in "
              "combat, turning the tables on your foes with a resolute and controlled counterattack.")
    modifier = AggregateModifier(
        TagMod(Tag.BlockedAlwaysReflect),
    )
    max_count = 1
    classes = {Classes.FIGHTER}


class Impale(RarePerk):
    _descr = ("A more powerful attack with an increased chance of breaking through the target's defense. "
              "Can only be used with swords and spears.")
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    max_count = 1
    classes = {Classes.FIGHTER}


class CriticalStrike(RarePerk):
    _descr = ("Grants a chance to do double physical damage with your attacks.)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    max_count = 1
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


















