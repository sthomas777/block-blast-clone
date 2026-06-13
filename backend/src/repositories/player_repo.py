from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.player import Player


@dataclass
class PlayerRepository:
    session: AsyncSession

    async def create(self, username: str, hashed_password: str) -> Player:
        player = Player(username=username, hashed_password=hashed_password)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def get_by_username(self, username: str) -> Player | None:
        result = await self.session.execute(
            select(Player).where(Player.username == username),
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, player_id: int) -> Player | None:
        result = await self.session.execute(
            select(Player).where(Player.player_id == player_id),
        )
        return result.scalar_one_or_none()
