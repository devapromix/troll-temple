from __future__ import annotations

from random import randrange, choice
from typing import Type

from mobs.perks.perk import *
from utils.random_help import *


class PerksContainer:
    NEW_PERKS_COUNT = 3
    NEW_PERKS_COUNT_WIZARD = 10
    RARITY_CHANCES = {
        PerkRarity.USUALLY: 8,
        PerkRarity.RARE: 4,
        PerkRarity.LEGEND: 1,
    }

    def __init__(self, player):
        self.__player = player
        self.__perks = dict()

    def generate_new_perks(self) -> List[Perk]:
        import mobs.perks.fighter_perks
        import mobs.perks.perks
        filtered_by_class = list(filter(lambda x: self.__check_perk(x), Perk.ALL))
        if self.__player.level % 5 == 0 and self.__player.level != 1:
            filtered_by_class = list(filter(lambda x: x.rarity == PerkRarity.LEGEND, filtered_by_class))
        boxes = [ChoiceBox(obj=cls, weight=self.RARITY_CHANCES[cls.rarity]) for cls in filtered_by_class]
        sample = weighted_sample(boxes, self.NEW_PERKS_COUNT
        if not self.__player.wizard else self.NEW_PERKS_COUNT_WIZARD)
        return [x() for x in sample]

    def teach(self, perk: Perk) -> None:
        assert self.__check_perk(perk)
        current = self.__perks.get(perk.name(), 0)
        self.__perks[perk.name()] = current + 1
        perk.use(self.__player)

    def __check_perk(self, perk: Perk | Type) -> bool:
        current = self.__perks.get(perk.name(), 0)
        return (len(perk.classes) == 0 or self.__player.game_class in perk.classes) and current < perk.max_count and perk.level_requirement <= self.__player.level
