from fastapi import APIRouter, Depends

from backend.src.core.dependencies import get_game_service
from backend.src.schemas.game import (
    PlaceShapeRequest,
    PlaceShapeResponse,
    GameStateResponse,
    GameStateMLResponse,
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
    return service.get_game(game_id)


@router.post("/{game_id}/place", response_model=PlaceShapeResponse)
def place_shape(
    game_id: str,
    request: PlaceShapeRequest,
    service: GameService = Depends(get_game_service),
) -> PlaceShapeResponse:
    return service.place_shape(
        game_id,
        request.shape_index,
        request.row,
        request.col,
    )


@router.get("/{game_id}/ml_state", response_model=GameStateMLResponse)
def get_ml_state(
    game_id: str,
    service: GameService = Depends(get_game_service),
) -> GameStateMLResponse:
    return service.get_ml_state(game_id)
