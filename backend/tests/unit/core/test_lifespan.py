from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.src.core import lifespan as lifespan_module
from backend.src.core.database import Base
from backend.src.core.lifespan import lifespan

pytestmark = pytest.mark.anyio


def _make_fake_engine() -> tuple[MagicMock, MagicMock]:
    conn = MagicMock()
    conn.run_sync = AsyncMock()

    begin_cm = MagicMock()
    begin_cm.__aenter__ = AsyncMock(return_value=conn)
    begin_cm.__aexit__ = AsyncMock(return_value=False)

    engine = MagicMock()
    engine.begin = MagicMock(return_value=begin_cm)
    engine.dispose = AsyncMock()
    return engine, conn


async def test_lifespan_creates_tables_on_startup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, conn = _make_fake_engine()
    monkeypatch.setattr(lifespan_module, "engine", engine)

    async with lifespan(MagicMock()):
        conn.run_sync.assert_awaited_once_with(Base.metadata.create_all)


async def test_lifespan_disposes_engine_on_shutdown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, _ = _make_fake_engine()
    monkeypatch.setattr(lifespan_module, "engine", engine)

    async with lifespan(MagicMock()):
        # Engine must stay alive while the app is serving.
        engine.dispose.assert_not_awaited()

    engine.dispose.assert_awaited_once()


async def test_lifespan_creates_before_yield_and_disposes_after(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, conn = _make_fake_engine()
    monkeypatch.setattr(lifespan_module, "engine", engine)

    async with lifespan(MagicMock()):
        # By the time control is yielded, tables exist and nothing is disposed.
        conn.run_sync.assert_awaited_once()
        engine.dispose.assert_not_awaited()

    conn.run_sync.assert_awaited_once()
    engine.dispose.assert_awaited_once()
