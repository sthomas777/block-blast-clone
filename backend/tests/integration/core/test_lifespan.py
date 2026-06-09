from unittest.mock import MagicMock

import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from backend.src.core import lifespan as lifespan_module
from backend.src.core.database import Base
from backend.src.core.lifespan import lifespan
from backend.src.models.game_session import GameSession
from backend.src.models.player import Player
from backend.src.models.score import Score

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def test_lifespan_creates_schema_in_real_db(
    postgres_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = create_async_engine(postgres_url)
    # Start from an empty schema so the assertion proves lifespan built it.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    monkeypatch.setattr(lifespan_module, "engine", engine)

    expected = {Player.__tablename__, GameSession.__tablename__, Score.__tablename__}

    async with lifespan(MagicMock()):
        async with engine.connect() as conn:
            tables = await conn.run_sync(lambda c: set(inspect(c).get_table_names()))
        assert expected <= tables

    # lifespan disposes the (patched) engine on exit; a fresh engine can still
    # connect, confirming the tables persisted.
    verify_engine = create_async_engine(postgres_url)
    async with verify_engine.connect() as conn:
        tables_after = await conn.run_sync(lambda c: set(inspect(c).get_table_names()))
    await verify_engine.dispose()

    assert expected <= tables_after
