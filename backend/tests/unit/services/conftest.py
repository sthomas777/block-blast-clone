import pytest
from backend.src.game.session import GameSession


@pytest.fixture
def test_game_session():
    return GameSession()


@pytest.fixture
def test_game_session_started():
    session = GameSession()
    session.start()
    return session
