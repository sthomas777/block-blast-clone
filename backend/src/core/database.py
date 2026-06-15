import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.secrets import read_secret

# DATABASE_URL may be provided whole (local dev / CI) or assembled from
# individual parts with the password stored as a Compose secret.
DATABASE_URL: str = os.environ.get("DATABASE_URL") or (
    "postgresql+asyncpg://"
    f"{read_secret('db_user')}:"
    f"{read_secret('db_password')}@"
    f"{os.environ.get('DB_HOST', 'localhost')}:"
    f"{os.environ.get('DB_PORT', '5432')}/"
    f"{read_secret('db_name')}"
)

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
