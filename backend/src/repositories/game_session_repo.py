from datetime import datetime
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.game_session import GameSession


@dataclass
class GameSessionRepository:
    session: AsyncSession

    async def save_game(
        self,
        player_id: int,
        session_id: int,
        final_grid: list[list[int | str]],
        lines_cleared: int,
        shapes_placed: int,
        status: int,
        started_at: datetime,
        ended_at: datetime,
    ) -> GameSession:
        game_session = GameSession(
            player_id=player_id,
            session_id=session_id,
            final_grid=final_grid,
            lines_cleared=lines_cleared,
            shapes_placed=shapes_placed,
            status=status,
            started_at=started_at,
            ended_at=ended_at,
        )
        self.session.add(game_session)
        await self.session.commit()
        await self.session.refresh(game_session)
        return game_session
