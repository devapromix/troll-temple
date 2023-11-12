from enum import Enum

from common.utils import Register
from common.modifiers.modifier import Modifier


class PerkRarity(Enum):
    USUALLY = 0,
    RARE = 1,
    LEGEND = 2,


class Perk(object, metaclass=Register):
    ALL = []
    ABSTRACT = True
    modifier = Modifier()
    rarity = PerkRarity.USUALLY
    max_count = 10
    level_requirement = 0
    _name = None
    name = __name__ if _name is None else _name
    _descr = "Unknown"
    classes = {}

    @property
    @classmethod
    def name(cls):
        return cls.__name__ if cls._name is None else cls._name

    @property
    def name(self):
        return type(self).__name__ if self._name is None else self._name

    @property
    def descr(self):
        return self._descr

    def __repr__(self):
        return self.name

    def use(self, mob):
        self.modifier.commit(mob)


class RarePerk(Perk):
    ABSTRACT = True
    rarity = PerkRarity.RARE
    level_requirement = 3


class LegendPerk(Perk):
    ABSTRACT = True
    rarity = PerkRarity.LEGEND
    max_count = 1
    level_requirement = 5