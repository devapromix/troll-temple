from common.game_class import Game
from common.modifiers.modifier import Modifier
from mobs.effects.effect import Effect
from mobs.effects.effects_container import EffectsContainer
from mobs.effects.uni_effect import UniEffect
from mobs.player import *
from tests.test_effect import create_mock


class TestEffect(Effect):
    modifier = create_mock()
    max_turns = 5


def test_effects_container_effect_lifetime():
    mob = Player(0, Classes.FIGHTER)
    effects = EffectsContainer(mob)
    effect = TestEffect()

    effects.add(effect)
    assert effect in effects
    for _ in range(0, 4):
        effects.act()
    assert effect in effects
    for _ in range(0, 4):
        effects.act()
    assert effect not in effects

def test_effects_container_uni_effect_simultaneously():
    mob = Player(0, Classes.FIGHTER)
    effects = mob.effects

    first = UniEffect(Modifier(), 5)
    effects.add(first)
    effects.act()
    assert first in effects

    second = UniEffect(Modifier(), 5)
    effects.add(second)
    effects.act()
    assert first in effects
    assert second in effects

    for _ in range(4):
        effects.act()

    assert first not in effects
    assert second in effects

    effects.act()
    assert second not in effects


def test_effects_container_uni_effect_max_turn():
    effect1 = UniEffect(Modifier(), 5)
    effect2 = UniEffect(Modifier(), 1)
    assert effect1.max_turns == 5
    assert effect1.max_turns != effect2.max_turns