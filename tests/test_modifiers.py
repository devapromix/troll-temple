from common.modifier import *
from mobs.player import *


def test_add_max_hp_commit_test():
    value = 10
    mod = AddMaxHp(value)
    player = Player(0, FIGHTER)

    old_hp = player.max_hp
    mod.commit(player)
    assert old_hp + value == player.max_hp

