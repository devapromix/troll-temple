from random import randrange, choice

from mobs.perks.perk import *
from mobs.perks.perks import *


class PerksContainer:
    NEW_PERKS_COUNT = 5

    def __init__(self, player):
        self.__player = player
        self.__perks = dict()

    def generate_new_perks(self):
        filtered_by_class = list(filter(lambda x: self.__check_perk(x), Perk.ALL))
        return [choice(filtered_by_class)() for _ in range(self.NEW_PERKS_COUNT)]

    def teach(self, perk: Perk):
        assert self.__check_perk(perk)
        current = self.__perks.get(perk.name, 0)
        self.__perks[perk.name] = current + 1
        perk.use(self.__player)

    def __check_perk(self, perk: Perk):
        current = self.__perks.get(perk.name, 0)
        return (len(perk.classes) == 0 or self.__player.game_class in perk.classes) and current < perk.max_count
