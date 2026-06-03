from pydantic import BaseModel, Field

from backend.src.game.session import GameState
from backend.src.models.shape import BlockBlastShape


class PlaceShapeRequest(BaseModel):
    shape_index: int = Field(
        ge=0,
        le=2,
        description="Which of the 3 available blocks to place",
    )
    row: int = Field(ge=0, le=7, description="Grid row (0=top, 7=bottom)")
    col: int = Field(ge=0, le=7, description="Grid column (0=left, 7=right)")


class GameStateResponse(BaseModel):
    game_id: str
    grid: list[list[int | str]]
    score: int
    shape: list[BlockBlastShape]
    status: GameState
    game_over: bool


class GameStateMLResponse(BaseModel):
    grid: list[list[int | str]]
    score: int
    shape: list[BlockBlastShape]
    game_over: bool
