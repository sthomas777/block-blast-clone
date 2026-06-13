from pydantic import TypeAdapter

from src.schemas.game import (
    ClientMessage,
    GameStateResponse,
    NewGameCommand,
    PlaceShapeCommand,
)
from src.services.game_service import GameService, InvalidGameID

# Built once at import time. Validates a raw dict into the right command model
# based on its "command_type" discriminator, raising ValidationError on bad input.
_client_adapter: TypeAdapter[ClientMessage] = TypeAdapter(ClientMessage)


def dispatch(raw: dict, game_id: str | None, service: GameService) -> GameStateResponse:
    command = _client_adapter.validate_python(raw)

    match command:
        case NewGameCommand():
            return service.create_game()
        case PlaceShapeCommand():
            if game_id is None:
                raise InvalidGameID("No active game; send a new_game command first")
            return service.place_shape(
                game_id,
                command.shape_index,
                command.row,
                command.col,
            )
