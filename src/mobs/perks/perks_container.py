from random import randrange, choice

from mobs.perks.perk import *
from mobs.perks.perks import *


class PerksContainer:
    def __init__(self, player):
        self.__perks = []
        self.__player = player

    def generate_new_perks(self):
        filtered_by_class = list(filter(lambda x: len(x.classes) == 0 or self.__player.game_class in x.classes, Perk.ALL))
        return [choice(filtered_by_class)() for _ in range(3)]

    def teach(self, perk):
        perk.use(self.__player)
