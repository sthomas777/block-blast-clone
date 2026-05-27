from fastapi import APIRouter, HTTPException, Depends

from backend.src.core.dependencies import get_game_service
from backend.src.game.session import GameState
from backend.src.services.game_service import GameService

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/new")
def new_game(
    service: GameService = Depends(get_game_service),
) -> dict[str, str | GameState]:
    return service.create_game()


@router.get("/{game_id}")
def get_game(
    game_id: str,
    service: GameService = Depends(get_game_service),
) -> dict[str, str | GameState]:
    if game_id not in service.games:
        raise HTTPException(status_code=404, detail="Game not found")
    return service.get_game(game_id)
