from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.database import get_session
from backend.src.main import app
from backend.src.models.game_session import GameSession
from backend.src.repositories.score_repo import ScoreRepository

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


@pytest.fixture
async def db_client(session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def _override_get_session() -> AsyncGenerator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = _override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


async def test_register_token_me_round_trip_against_real_db(
    db_client: AsyncClient,
) -> None:
    register = await db_client.post(
        "/api/auth/register",
        json={"username": "test", "password": "supersecret"},
    )
    assert register.status_code == 200
    player_id = register.json()["player_id"]

    token_response = await db_client.post(
        "/api/auth/token",
        data={"username": "test", "password": "supersecret"},
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    me = await db_client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    body = me.json()
    assert body["username"] == "test"
    assert body["player_id"] == player_id


async def test_register_duplicate_username_against_real_db(
    db_client: AsyncClient,
) -> None:
    first = await db_client.post(
        "/api/auth/register",
        json={"username": "test", "password": "supersecret"},
    )
    assert first.status_code == 200

    duplicate = await db_client.post(
        "/api/auth/register",
        json={"username": "test", "password": "anothersecret"},
    )
    assert duplicate.status_code == 409


async def test_token_with_bad_password_against_real_db(
    db_client: AsyncClient,
) -> None:
    await db_client.post(
        "/api/auth/register",
        json={"username": "test", "password": "supersecret"},
    )

    bad = await db_client.post(
        "/api/auth/token",
        data={"username": "test", "password": "wrongpassword"},
    )
    assert bad.status_code == 401


async def test_get_my_scores_against_real_db(
    db_client: AsyncClient,
    session: AsyncSession,
) -> None:
    register = await db_client.post(
        "/api/auth/register",
        json={"username": "test", "password": "supersecret"},
    )
    player_id = register.json()["player_id"]

    token_response = await db_client.post(
        "/api/auth/token",
        data={"username": "test", "password": "supersecret"},
    )
    token = token_response.json()["access_token"]

    # Seed a game session (FK target) and two scores for this player.
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

    score_repo = ScoreRepository(session)
    await score_repo.save_score(player_id, game_session.session_id, 100, 1)
    await score_repo.save_score(player_id, game_session.session_id, 300, 3)

    response = await db_client.get(
        "/api/scores/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert [s["score"] for s in body] == [300, 100]
    assert all(s["player_id"] == player_id for s in body)
