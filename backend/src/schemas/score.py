from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    score_id: int
    player_id: int
    session_id: int | None
    score: int
    lines_cleared: int
    achieved_at: datetime
