from common.game_class import Game

from mobs.perks.perks import Agility


def test_perk_name():
    perk = Agility()
    assert perk.name() == 'Agility'
    name = Agility.name()
    assert name == 'Agility'
    assert name == perk.name()
