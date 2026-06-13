from collections.abc import Sequence

from fastapi import APIRouter, Depends

from src.core.dependencies import get_authenticated_player, get_score_repo
from src.models.player import Player
from src.models.score import Score
from src.repositories.score_repo import ScoreRepository
from src.schemas.score import ScoreResponse

router = APIRouter(prefix="/api/scores")


@router.get("/me", response_model=list[ScoreResponse])
async def get_my_scores(
    player: Player = Depends(get_authenticated_player),
    score_repo: ScoreRepository = Depends(get_score_repo),
) -> Sequence[Score]:
    return await score_repo.get_player_scores(player.player_id)
