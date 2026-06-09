from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from backend.src.core import database
from backend.src.core.database import Base, get_session


def test_base_is_declarative_base() -> None:
    assert issubclass(Base, DeclarativeBase)


@pytest.mark.anyio
async def test_get_session_yields_async_session() -> None:
    agen = get_session()
    session = await agen.__anext__()
    try:
        assert isinstance(session, AsyncSession)
    finally:
        await agen.aclose()


@pytest.mark.anyio
async def test_get_session_closes_session_on_exhaustion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = MagicMock()
    session_cm = MagicMock()
    session_cm.__aenter__ = AsyncMock(return_value=session)
    session_cm.__aexit__ = AsyncMock(return_value=False)
    monkeypatch.setattr(database, "async_session", MagicMock(return_value=session_cm))

    agen = get_session()
    yielded = await agen.__anext__()

    assert yielded is session
    # Still open while the caller holds the session.
    session_cm.__aexit__.assert_not_awaited()

    with pytest.raises(StopAsyncIteration):
        await agen.__anext__()

    # Exhausting the generator must close the session via the context manager.
    session_cm.__aexit__.assert_awaited_once()
