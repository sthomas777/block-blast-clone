from typing import Annotated, Literal

from pydantic import BaseModel, Field

from backend.src.game.session import GameState
from backend.src.models.shape import BlockBlastShape


class NewGameCommand(BaseModel):
    command_type: Literal["new_game"]


class PlaceShapeCommand(BaseModel):
    command_type: Literal["place_shape"]
    shape_index: int = Field(
        ge=0,
        le=2,
        description="Which of the 3 available blocks to place",
    )
    row: int = Field(ge=0, le=7, description="Grid row (0=top, 7=bottom)")
    col: int = Field(ge=0, le=7, description="Grid column (0=left, 7=right)")


# PEP 695 type alias (Python 3.12). The discriminator tells Pydantic to
# route on the "command_type" field instead of trying each member in turn.
type ClientMessage = Annotated[
    NewGameCommand | PlaceShapeCommand,
    Field(discriminator="command_type"),
]


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


class ErrorResponse(BaseModel):
    command_type: Literal["error"] = "error"
    code: Literal["validation_error", "game_error", "internal_error"]
    message: str
