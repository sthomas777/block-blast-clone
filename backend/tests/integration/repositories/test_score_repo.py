import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.game_session import GameSession
from src.models.player import Player
from src.repositories.score_repo import ScoreRepository

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def _seed_player(session: AsyncSession, username: str = "test") -> int:
    player = Player(username=username, hashed_password="hashed-password")
    session.add(player)
    await session.commit()
    await session.refresh(player)
    return player.player_id


async def _seed_game_session(session: AsyncSession, player_id: int) -> int:
    game_session = GameSession(
        player_id=player_id,
        final_grid=[[0]],
        shapes_placed=0,
        lines_cleared=0,
        status=0,
        ended_at=None,
    )
    session.add(game_session)
    await session.commit()
    await session.refresh(game_session)
    return game_session.session_id


async def test_save_score_persists_and_returns(session: AsyncSession) -> None:
    player_id = await _seed_player(session)
    session_id = await _seed_game_session(session, player_id)
    repo = ScoreRepository(session)

    score = await repo.save_score(
        player_id=player_id,
        session_id=session_id,
        player_score=1500,
        lines_cleared=4,
    )

    assert score.score_id is not None
    assert score.player_id == player_id
    assert score.session_id == session_id
    assert score.score == 1500
    assert score.lines_cleared == 4
    assert score.achieved_at is not None


async def test_get_top_scores_orders_by_score_desc(session: AsyncSession) -> None:
    player_id = await _seed_player(session)
    session_id = await _seed_game_session(session, player_id)
    repo = ScoreRepository(session)

    await repo.save_score(player_id, session_id, player_score=100, lines_cleared=1)
    await repo.save_score(player_id, session_id, player_score=300, lines_cleared=3)
    await repo.save_score(player_id, session_id, player_score=200, lines_cleared=2)

    top = await repo.get_top_scores()

    assert [s.score for s in top] == [300, 200, 100]


async def test_get_top_scores_respects_limit(session: AsyncSession) -> None:
    player_id = await _seed_player(session)
    session_id = await _seed_game_session(session, player_id)
    repo = ScoreRepository(session)

    for value in (100, 200, 300, 400):
        await repo.save_score(
            player_id,
            session_id,
            player_score=value,
            lines_cleared=1,
        )

    top = await repo.get_top_scores(limit=2)

    assert [s.score for s in top] == [400, 300]


async def test_get_top_scores_empty_when_no_scores(session: AsyncSession) -> None:
    repo = ScoreRepository(session)

    assert await repo.get_top_scores() == []


async def test_get_top_scores_spans_multiple_players(session: AsyncSession) -> None:
    player_one = await _seed_player(session, "test-one")
    player_two = await _seed_player(session, "test-two")
    session_one = await _seed_game_session(session, player_one)
    session_two = await _seed_game_session(session, player_two)
    repo = ScoreRepository(session)

    await repo.save_score(player_one, session_one, player_score=250, lines_cleared=2)
    await repo.save_score(player_two, session_two, player_score=900, lines_cleared=5)

    top = await repo.get_top_scores()

    assert [s.score for s in top] == [900, 250]


async def test_get_player_scores_returns_only_that_player(
    session: AsyncSession,
) -> None:
    player_one = await _seed_player(session, "test-one")
    player_two = await _seed_player(session, "test-two")
    session_one = await _seed_game_session(session, player_one)
    session_two = await _seed_game_session(session, player_two)
    repo = ScoreRepository(session)

    await repo.save_score(player_one, session_one, player_score=100, lines_cleared=1)
    await repo.save_score(player_one, session_one, player_score=300, lines_cleared=3)
    await repo.save_score(player_two, session_two, player_score=999, lines_cleared=9)

    scores = await repo.get_player_scores(player_one)

    assert all(s.player_id == player_one for s in scores)
    assert [s.score for s in scores] == [300, 100]


async def test_get_player_scores_respects_limit(session: AsyncSession) -> None:
    player_id = await _seed_player(session)
    session_id = await _seed_game_session(session, player_id)
    repo = ScoreRepository(session)

    for value in (100, 200, 300):
        await repo.save_score(
            player_id,
            session_id,
            player_score=value,
            lines_cleared=1,
        )

    scores = await repo.get_player_scores(player_id, limit=1)

    assert [s.score for s in scores] == [300]


async def test_get_player_scores_empty_for_unknown_player(
    session: AsyncSession,
) -> None:
    repo = ScoreRepository(session)

    assert await repo.get_player_scores(999_999) == []


async def test_get_top_scores_keeps_tied_scores_grouped(session: AsyncSession) -> None:
    player_id = await _seed_player(session)
    session_id = await _seed_game_session(session, player_id)
    repo = ScoreRepository(session)

    high_a = await repo.save_score(
        player_id,
        session_id,
        player_score=200,
        lines_cleared=2,
    )
    high_b = await repo.save_score(
        player_id,
        session_id,
        player_score=200,
        lines_cleared=2,
    )
    await repo.save_score(player_id, session_id, player_score=100, lines_cleared=1)

    top = await repo.get_top_scores()
    values = [s.score for s in top]

    # Ordering is non-increasing and the two tied 200s rank above the 100,
    # without asserting a specific (unspecified) tie-break order between them.
    assert values == [200, 200, 100]
    assert all(a >= b for a, b in zip(values, values[1:], strict=False))
    assert {top[0].score_id, top[1].score_id} == {high_a.score_id, high_b.score_id}
