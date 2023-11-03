from common.game import Game
from common.modifiers.aggregate_modifier import AggregateModifier
from common.modifiers.attrib_mod import AddMaxHp
from common.modifiers.fight_for_life import FightForLife
from common.modifiers.mod import Mod
from common.modifiers.modifier import Modifier
from mobs.player import *
import pytest


@pytest.mark.parametrize("mod,attr_name", [(Mod("armor", 15), "armor"),
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
    mods = AggregateModifier(AddMaxHp(max_hp_bonus), Mod('armor', armor_bonus))
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

def test_union_mod():
    mod = Modifier()
    mod += Modifier()
    assert isinstance(mod, Modifier)

    mod += Mod('speed', 1)
    assert isinstance(mod, Mod)

    mod += Mod('speed', 2)
    assert isinstance(mod, AggregateModifier)

    mod += AggregateModifier(Mod('armor', 3), Mod('accuracy', 15))
    assert isinstance(mod, AggregateModifier)
    assert len(mod.mods) == 4

def test_union_the_same():
    mod = Modifier()
    mod += Mod('armor', 1)
    mod += Mod('speed', 1)
    mod += Mod('speed', 2)
    assert len(mod) == 2