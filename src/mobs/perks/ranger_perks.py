from .perk import *
from ..player import Classes


class EagleEye(Perk):
    _name = "eagle eye"
    _descr = "The eagle eye allows you to increase the distance from which you can shoot at a target"
    modifier = Mod('radius', 1)
    max_count = 2
    classes = {Classes.RANGER}


class MagicArrow(RarePerk):
    _descr = ("The archer has a 10% chance of creating a magic arrow using his mana. "
              "In this case, the arrow from the quiver is not consumed. This can be "
              "useful if you don't have many arrows.")
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    max_count = 1
    classes = {Classes.RANGER}



























