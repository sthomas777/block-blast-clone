from collections.abc import Sequence

from fastapi import APIRouter, Depends

from backend.src.core.dependencies import get_authenticated_player, get_score_repo
from backend.src.models.player import Player
from backend.src.models.score import Score
from backend.src.repositories.score_repo import ScoreRepository
from backend.src.schemas.score import ScoreResponse

router = APIRouter(prefix="/api/scores")


@router.get("/me", response_model=list[ScoreResponse])
async def get_my_scores(
    player: Player = Depends(get_authenticated_player),
    score_repo: ScoreRepository = Depends(get_score_repo),
) -> Sequence[Score]:
    return await score_repo.get_player_scores(player.player_id)
