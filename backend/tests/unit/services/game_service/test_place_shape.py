import pytest
from backend.src.services.game_service import (
    GameService,
    InvalidGameID,
    InvalidPosition,
)
from backend.tests.unit.services.data.test_place_shape_data import (
    expected_placement_response,
)


def test_place_shape(test_game_session_started) -> None:
    game = GameService()
    game.games["1111-2222-3333-4444"] = test_game_session_started

    actual = game.place_shape("1111-2222-3333-4444", 0, 3, 3)

    assert len(actual.shape) == len(expected_placement_response.shape)


def test_place_shape_invalid_game_id() -> None:
    """Test that place_shape raises InvalidGameID for non-existent game"""
    game = GameService()

    with pytest.raises(InvalidGameID, match="Invalid game id"):
        game.place_shape("non-existent-id", 0, 3, 3)


def test_place_shape_invalid_shape_index(test_game_session_started) -> None:
    game = GameService()
    game.games["1111-2222-3333-4444"] = test_game_session_started

    with pytest.raises(InvalidPosition, match="Invalid shape has been chosen"):
        game.place_shape("1111-2222-3333-4444", 999, 3, 3)
