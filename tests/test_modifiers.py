from common.game import Game
from common.modifiers.add_armor import AddArmor
from common.modifiers.add_max_hp import AddMaxHp
from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.fight_for_life import FightForLife
from common.modifiers.mod import Mod
from mobs.player import *
import pytest


@pytest.mark.parametrize("mod,attr_name", [(AddArmor(15), "armor"),
                                           (Mod("armor", 15), "armor"),
                                           (Mod('speed', 10), 'speed')])
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

    old_hp = player.life.cur
    mod.commit(player)

    assert old_hp + value == player.life.max


def test_aggregate_modifier():
    max_hp_bonus = 10
    armor_bonus = 6
    mods = AggregateModifier(AddMaxHp(max_hp_bonus), AddArmor(armor_bonus))
    mob = Player(0, FIGHTER)

    old_hp = mob.life.cur
    old_armor = mob.armor
    mods.commit(mob)

    assert old_hp + max_hp_bonus == mob.life.max
    assert old_armor + armor_bonus == mob.armor


def test_fight_for_life():
    mod = FightForLife()
    mob = Player(0, FIGHTER)

    mob.hp = mob.life.cur - 1
    mod.act(mob)
    assert mob.hp == mob.life.max - 1

    mob.hp = 1
    mod.act(mob)
    assert mob.life.cur != 1
