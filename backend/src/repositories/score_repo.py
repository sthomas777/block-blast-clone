from dataclasses import dataclass

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.player import Player
from backend.src.models.score import Score


@dataclass
class ScoreRepository:
    session: AsyncSession

    async def save_score(
        self,
        player_id: int,
        session_id: int | None,
        player_score: int,
        lines_cleared: int,
    ) -> Score:
        score = Score(
            player_id=player_id,
            session_id=session_id,
            score=player_score,
            lines_cleared=lines_cleared,
        )
        self.session.add(score)
        await self.session.commit()
        await self.session.refresh(score)
        return score

    async def get_top_scores(self, limit: int = 10) -> Sequence[Score]:
        result = await self.session.execute(
            select(Score)
            .join(Player, Score.player_id == Player.player_id)
            .order_by(Score.score.desc())
            .limit(limit),
        )
        return result.scalars().all()

    async def get_player_scores(
        self,
        player_id: int,
        limit: int = 10,
    ) -> Sequence[Score]:
        result = await self.session.execute(
            select(Score)
            .where(Score.player_id == player_id)
            .order_by(Score.score.desc())
            .limit(limit),
        )
        return result.scalars().all()
