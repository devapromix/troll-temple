from common.game import Game
from items.items import ShortStaff
from mobs.player import *


def test_item_use_mods():
    player_with = Player(0, FIGHTER)
    player_with.can_use_staff = True
    player_with.equip(ShortStaff())
    player_without = Player(0, FIGHTER)

    assert player_without.magic != player_with.magic
    assert player_without.mana != player_with.mana
