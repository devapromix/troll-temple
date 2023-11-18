from .perk import *
from ..player import Classes


class MagicArrow(RarePerk):
    _descr = ("The archer has a 10% chance of creating a magic arrow using his mana. "
              "In this case, the arrow from the quiver is not consumed. This can be "
              "useful if you don't have many arrows.")
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    max_count = 1
    classes = {Classes.RANGER}


























