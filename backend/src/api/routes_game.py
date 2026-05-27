from fastapi import APIRouter, HTTPException, Depends

from backend.src.core.dependencies import get_game_service
from backend.src.schemas.game import (
    PlaceShapeRequest,
    PlaceShapeResponse,
    GameStateResponse,
)
from backend.src.services.game_service import GameService

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/new", response_model=GameStateResponse)
def new_game(
    service: GameService = Depends(get_game_service),
) -> GameStateResponse:
    return service.create_game()


@router.get("/{game_id}", response_model=GameStateResponse)
def get_game(
    game_id: str,
    service: GameService = Depends(get_game_service),
) -> GameStateResponse:
    if game_id not in service.games:
        raise HTTPException(status_code=404, detail="Game not found")
    return service.get_game(game_id)


@router.post("/{game_id}/place", response_model=PlaceShapeResponse)
def place_shape(
    game_id: str,
    request: PlaceShapeRequest,
    service: GameService = Depends(get_game_service),
) -> PlaceShapeResponse:
    if game_id not in service.games:
        raise HTTPException(status_code=404, detail="Game not found")

    placing_shape = service.place_shape(
        game_id,
        request.shape_index,
        request.row,
        request.col,
    )
    if not placing_shape:
        raise HTTPException(status_code=400, detail="Invalid placement")

    return placing_shape
