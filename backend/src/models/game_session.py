from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


from backend.src.core.database import Base


class GameSession(Base):
    __tablename__ = "gamesessions"

    session_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.player_id"))
    final_grid: Mapped[list[list[int | str]]] = mapped_column(JSONB, nullable=False)
    shapes_placed: Mapped[int] = mapped_column(Integer, nullable=False)
    lines_cleared: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
