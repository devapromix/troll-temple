from unittest.mock import Mock

from mobs.effects.effect import Effect
from mobs.player import *

class TestEffect(Effect):
    modifier = Mock()
    max_turns = 5

def test_base_effect():
    effect = TestEffect()
    mob = Player(0, FIGHTER)
    effect.register(mob)
    for _ in range(0, 10):
        effect.act()

    TestEffect.modifier.commit.assert_called_once_with(mob)
    TestEffect.modifier.rollback.assert_called_once_with(mob)
    assert TestEffect.modifier.act.call_count == 5
