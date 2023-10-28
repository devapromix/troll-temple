from common.modifier import *
from mobs.player import *
import pytest

@pytest.mark.parametrize("mod,attr_name", [(AddMaxHp(10), "max_hp"), (AddMaxHp(15), "max_hp")])
def test_modifier_rollback(mod, attr_name):
    mob = Player(0, FIGHTER)

    value_before_commit = getattr(mob, attr_name)
    mod.commit(mob)
    value_after_commit = getattr(mob, attr_name)
    mod.rollback(mob)
    value_after_rollback = getattr(mob, attr_name)

    assert value_before_commit == value_after_rollback
    assert value_before_commit != value_after_commit
    assert value_after_rollback != value_after_commit

def test_add_max_hp_commit_test():
    value = 10
    mod = AddMaxHp(value)
    player = Player(0, FIGHTER)

    old_hp = player.max_hp
    mod.commit(player)
    assert old_hp + value == player.max_hp

