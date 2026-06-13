import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.player_repo import PlayerRepository

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def test_create_persists_and_returns_player(session: AsyncSession) -> None:
    repo = PlayerRepository(session)

    player = await repo.create("test", "hashed-password")

    assert player.player_id is not None
    assert player.username == "test"
    assert player.hashed_password == "hashed-password"
    assert player.total_score == 0
    assert player.created_at is not None


async def test_get_by_username_returns_created_player(session: AsyncSession) -> None:
    repo = PlayerRepository(session)
    created = await repo.create("test", "hashed-password")

    fetched = await repo.get_by_username("test")

    assert fetched is not None
    assert fetched.player_id == created.player_id
    assert fetched.username == "test"


async def test_get_by_username_returns_none_when_missing(session: AsyncSession) -> None:
    repo = PlayerRepository(session)

    assert await repo.get_by_username("does-not-exist") is None


async def test_get_by_id_returns_created_player(session: AsyncSession) -> None:
    repo = PlayerRepository(session)
    created = await repo.create("test", "hashed-password")

    fetched = await repo.get_by_id(created.player_id)

    assert fetched is not None
    assert fetched.player_id == created.player_id
    assert fetched.username == "test"


async def test_get_by_id_returns_none_when_missing(session: AsyncSession) -> None:
    repo = PlayerRepository(session)

    assert await repo.get_by_id(999_999) is None


async def test_create_assigns_incrementing_ids(session: AsyncSession) -> None:
    repo = PlayerRepository(session)

    first = await repo.create("test-one", "hashed-password")
    second = await repo.create("test-two", "hashed-password")

    assert first.player_id != second.player_id


async def test_create_duplicate_username_raises(session: AsyncSession) -> None:
    repo = PlayerRepository(session)
    await repo.create("test", "hashed-password")

    with pytest.raises(IntegrityError):
        await repo.create("test", "another-password")
