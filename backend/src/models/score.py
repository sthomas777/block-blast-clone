from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


from backend.src.core.database import Base


class Score(Base):
    __tablename__ = "scores"

    score_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.player_id"))
    session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("gamesessions.session_id"),
    )
    score: Mapped[int] = mapped_column(BigInteger, default=0)
    lines_cleared: Mapped[int] = mapped_column(BigInteger, default=0)
    achieved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
