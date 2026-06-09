import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.src.core import database
from backend.src.core.database import get_session

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def test_get_session_yields_usable_session(
    postgres_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = create_async_engine(postgres_url)
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    monkeypatch.setattr(database, "async_session", maker)

    agen = get_session()
    session = await agen.__anext__()
    try:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1
    finally:
        await agen.aclose()

    await engine.dispose()
