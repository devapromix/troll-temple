from .perk import *
from ..player import Classes


class Poisoner(Perk):
    _name = "poisoner"
    _descr = "You discover new alchemy poisons and poison your enemies more effectively."
    ###modifier = Mod('poison', 1)
    max_count = 5
    classes = {Classes.THIEF}


class CloakOfShadows(RarePerk):
    _name = "cloak of shadows"
    _descr = ("Moving twice as long through the darkness, invisible to enemies, "
              "the thief can sneak past opponents or ambush unsuspecting victims.")
    ### player.invisible_cooldown = 20
    max_count = 1
    classes = {Classes.THIEF}


class PoisonResistance(RarePerk):
    _name = 'poison resistance'
    _descr = 'The character is immune to poisons.'
    max_count = 1
    ### player.immune = True
    classes = {Classes.THIEF}


class Bower(LegendPerk):
    _name = "bower"
    _descr = "You can use a ranged weapons and hit your enemies with it."
    ###player.can_use_bow = True
    classes = {Classes.THIEF}


























