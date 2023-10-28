from common.modifiers.add_armor import AddArmor
from common.modifiers.add_max_hp import AddMaxHp
from common.modifiers.aggregate_modifier import AggregateModifier
from mobs.player import *
import pytest

@pytest.mark.parametrize("mod,attr_name", [(AddMaxHp(10), "max_hp"), (AddArmor(15), "armor")])
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

def test_aggregate_modifier():
    max_hp_bonus = 10
    armor_bonus = 6
    mods = AggregateModifier(AddMaxHp(max_hp_bonus), AddArmor(armor_bonus))
    mob = Player(0, FIGHTER)

    old_hp = mob.max_hp
    old_armor = mob.armor
    mods.commit(mob)

    assert old_hp + max_hp_bonus == mob.max_hp
    assert old_armor + armor_bonus == mob.armor
