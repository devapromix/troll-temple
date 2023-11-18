from .perk import *
from ..player import Classes


class CloakOfShadows(RarePerk):
    _descr = ("Moving twice as long through the darkness, invisible to enemies, "
              "the thief can sneak past opponents or ambush unsuspecting victims.")
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    max_count = 1
    classes = {Classes.THIEF}


























