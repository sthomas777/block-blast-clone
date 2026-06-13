from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.game_session import GameSession
from src.models.player import Player
from src.repositories.game_session_repo import GameSessionRepository

pytestmark = [pytest.mark.anyio, pytest.mark.integration]

STARTED_AT = datetime(2024, 1, 1, 12, 0, 0)
ENDED_AT = datetime(2024, 1, 1, 12, 5, 30)


async def _create_player(session: AsyncSession, username: str = "player-one") -> Player:
    player = Player(username=username, hashed_password="hashed")
    session.add(player)
    await session.commit()
    await session.refresh(player)
    return player


async def test_save_game_returns_persisted_session(session: AsyncSession) -> None:
    player = await _create_player(session)
    repo = GameSessionRepository(session)

    saved = await repo.save_game(
        player_id=player.player_id,
        session_id=1,
        final_grid=[[0, 1], [1, 0]],
        lines_cleared=3,
        shapes_placed=7,
        status=2,
        started_at=STARTED_AT,
        ended_at=ENDED_AT,
    )

    assert saved.session_id == 1
    assert saved.player_id == player.player_id
    assert saved.lines_cleared == 3
    assert saved.shapes_placed == 7
    assert saved.status == 2
    assert saved.started_at == STARTED_AT
    assert saved.ended_at == ENDED_AT


async def test_save_game_row_is_readable_in_a_fresh_query(
    session: AsyncSession,
) -> None:
    player = await _create_player(session)
    repo = GameSessionRepository(session)

    await repo.save_game(
        player_id=player.player_id,
        session_id=42,
        final_grid=[[0]],
        lines_cleared=1,
        shapes_placed=1,
        status=1,
        started_at=STARTED_AT,
        ended_at=ENDED_AT,
    )

    # Drop the identity-map cache so the read hits the database, not the
    # instance returned by save_game.
    session.expunge_all()
    fetched = await session.get(GameSession, 42)

    assert fetched is not None
    assert fetched.player_id == player.player_id
    assert fetched.lines_cleared == 1
    assert fetched.shapes_placed == 1


async def test_save_game_round_trips_grid_json(session: AsyncSession) -> None:
    player = await _create_player(session)
    repo = GameSessionRepository(session)
    grid: list[list[int | str]] = [[0, 1, "red"], ["blue", 0, 1]]

    await repo.save_game(
        player_id=player.player_id,
        session_id=5,
        final_grid=grid,
        lines_cleared=0,
        shapes_placed=2,
        status=0,
        started_at=STARTED_AT,
        ended_at=ENDED_AT,
    )

    session.expunge_all()
    fetched = await session.get(GameSession, 5)

    assert fetched is not None
    assert fetched.final_grid == grid


async def test_save_game_persists_multiple_sessions(session: AsyncSession) -> None:
    player = await _create_player(session)
    repo = GameSessionRepository(session)

    first = await repo.save_game(
        player_id=player.player_id,
        session_id=100,
        final_grid=[[0]],
        lines_cleared=1,
        shapes_placed=1,
        status=1,
        started_at=STARTED_AT,
        ended_at=ENDED_AT,
    )
    second = await repo.save_game(
        player_id=player.player_id,
        session_id=200,
        final_grid=[[1]],
        lines_cleared=2,
        shapes_placed=2,
        status=2,
        started_at=STARTED_AT,
        ended_at=ENDED_AT,
    )

    assert first.session_id == 100
    assert second.session_id == 200
    assert await session.get(GameSession, 100) is not None
    assert await session.get(GameSession, 200) is not None
