import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.src.game.session import GameState
from backend.src.services.game_service import GameService

pytestmark = pytest.mark.anyio


def _make_score_repo() -> MagicMock:
    repo = MagicMock()
    repo.save_score = AsyncMock()
    return repo


def _make_game_over_session(score: int = 500) -> MagicMock:
    session = MagicMock()
    session.state = GameState.GAME_OVER
    session.get_score.return_value = score
    return session


async def test_end_game_does_nothing_for_unknown_game_id() -> None:
    service = GameService()
    score_repo = _make_score_repo()

    await service.end_game("nonexistent", score_repo, player_id=1)

    score_repo.save_score.assert_not_awaited()


async def test_end_game_does_nothing_when_not_game_over() -> None:
    service = GameService()
    score_repo = _make_score_repo()
    session = MagicMock()
    session.state = GameState.PLAYER_TURN  # not GAME_OVER
    service.games["abc"] = session

    await service.end_game("abc", score_repo, player_id=1)

    score_repo.save_score.assert_not_awaited()
    assert "abc" in service.games  # not cleaned up


async def test_end_game_cleans_up_without_saving_when_no_player_id() -> None:
    service = GameService()
    score_repo = _make_score_repo()
    service.games["abc"] = _make_game_over_session()

    await service.end_game("abc", score_repo)  # no player_id

    score_repo.save_score.assert_not_awaited()
    assert "abc" not in service.games


async def test_end_game_saves_score_and_cleans_up() -> None:
    service = GameService()
    score_repo = _make_score_repo()
    service.games["abc"] = _make_game_over_session(score=500)

    await service.end_game("abc", score_repo, player_id=7)

    score_repo.save_score.assert_awaited_once_with(
        player_id=7,
        session_id=None,
        player_score=500,
        lines_cleared=50,
    )
    assert "abc" not in service.games
