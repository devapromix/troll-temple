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
    __name = None
    __descr = ""
    classes = {}

    @property
    @classmethod
    def name(cls):
        return cls.__name__ if cls.__name is None else cls.__name

    @property
    def name(self):
        return type(self).__name__ if self.__name is None else self.__name

    @property
    def descr(self):
        return self.__descr

    def __repr__(self):
        return self.name

    def use(self, mob):
        self.modifier.commit(mob)