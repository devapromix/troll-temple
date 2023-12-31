from common.game_class import Game
from unittest.mock import Mock, MagicMock

from mobs.effects.effect import Effect
from mobs.player import *

def create_mock():
    mock = MagicMock()
    mock.configure_mock(descr='my_name')
    return mock

class TestEffect(Effect):
    modifier = create_mock()
    max_turns = 5

def test_base_effect():
    effect = TestEffect()
    mob = Player(0, Classes.FIGHTER)
    effect.register(mob)
    for _ in range(0, 10):
        effect.act()

    TestEffect.modifier.commit.assert_called_once_with(mob)
    TestEffect.modifier.rollback.assert_called_once_with(mob)
    assert TestEffect.modifier.act.call_count == 5
