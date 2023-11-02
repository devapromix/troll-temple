from common.game import Game

from tests.test_effect import create_mock
from utils.event import Event


def test_event():
    mock = create_mock()
    event = Event()

    event += lambda x: mock.firstSub(x)
    event += lambda x: mock.secondSub(x)
    event.invoke(1)

    mock.firstSub.assert_called_once_with(1)
    mock.secondSub.assert_called_once_with(1)
