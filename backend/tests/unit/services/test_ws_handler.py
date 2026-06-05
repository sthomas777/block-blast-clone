import pytest
from pydantic import ValidationError

from backend.src.schemas.game import GameStateResponse
from backend.src.services.game_service import GameService, InvalidGameID
from backend.src.services.ws_handler import dispatch


def test_new_game_creates_game() -> None:
    service = GameService()

    response = dispatch({"command_type": "new_game"}, None, service)

    assert isinstance(response, GameStateResponse)
    assert response.game_id in service.games


def test_place_shape_routes_to_service() -> None:
    service = GameService()
    game = dispatch({"command_type": "new_game"}, None, service)

    response = dispatch(
        {"command_type": "place_shape", "shape_index": 0, "row": 3, "col": 3},
        game.game_id,
        service,
    )

    assert isinstance(response, GameStateResponse)
    assert len(response.shape) == 2
    assert response.game_id == game.game_id


def test_place_shape_without_game_id_raises() -> None:
    service = GameService()

    with pytest.raises(InvalidGameID):
        dispatch(
            {"command_type": "place_shape", "shape_index": 0, "row": 3, "col": 3},
            None,
            service,
        )


def test_unknown_type_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        dispatch({"command_type": "does_not_exist"}, None, GameService())


def test_out_of_range_field_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        dispatch(
            {"command_type": "place_shape", "shape_index": 9, "row": 3, "col": 3},
            "any",
            GameService(),
        )


def test_missing_fields_raise_validation_error() -> None:
    with pytest.raises(ValidationError):
        dispatch({"command_type": "place_shape"}, "any", GameService())
