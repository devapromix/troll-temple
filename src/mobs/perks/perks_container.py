from random import randrange, choice

from mobs.perks.perk import *
from mobs.perks.perks import *
from utils.random_help import *


class PerksContainer:
    NEW_PERKS_COUNT = 5
    RARITY_CHANCES = {
        PerkRarity.USUALLY: 4,
        PerkRarity.RARE: 2,
        PerkRarity.LEGEND: 1,
    }

    def __init__(self, player):
        self.__player = player
        self.__perks = dict()

    def generate_new_perks(self) -> list[Perk]:
        filtered_by_class = list(filter(lambda x: self.__check_perk(x), Perk.ALL))
        filtered_by_class = [ChoiceBox(obj=cls, weight=self.RARITY_CHANCES[cls.rarity]) for cls in filtered_by_class]
        return [weighted_choice(filtered_by_class)() for _ in range(self.NEW_PERKS_COUNT)]

    def teach(self, perk: Perk) -> None:
        assert self.__check_perk(perk)
        current = self.__perks.get(perk.name, 0)
        self.__perks[perk.name] = current + 1
        perk.use(self.__player)

    def __check_perk(self, perk: Perk) -> bool:
        current = self.__perks.get(perk.name, 0)
        return (len(perk.classes) == 0 or self.__player.game_class in perk.classes) and current < perk.max_count
