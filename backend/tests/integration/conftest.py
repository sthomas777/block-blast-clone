from collections.abc import AsyncGenerator, Iterator

import pytest
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from backend.src.core.database import Base

# Hosts the destructive schema reset (drop_all) is ever allowed to touch.
# A testcontainer is always published on the local loopback interface.
_LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", ""}


def _assert_local(url: str) -> None:
    host = make_url(url).host or ""
    if host not in _LOCAL_HOSTS:
        raise RuntimeError(
            f"Refusing to run drop_all/create_all against non-local host {host!r}. "
            "This fixture is for throwaway test containers only.",
        )


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def postgres_url() -> Iterator[str]:
    with PostgresContainer("postgres:18", driver="asyncpg") as postgres:
        yield postgres.get_connection_url()


@pytest.fixture
async def session(postgres_url: str) -> AsyncGenerator[AsyncSession]:
    _assert_local(postgres_url)
    engine = create_async_engine(postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as db_session:
        yield db_session

    await engine.dispose()
