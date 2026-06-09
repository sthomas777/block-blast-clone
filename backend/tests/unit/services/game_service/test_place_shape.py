import pytest

from backend.src.game.session import GameState
from backend.src.models.shape import BlockBlastShape
from backend.src.schemas.game import GameStateResponse
from backend.src.services.game_service import (
    GameService,
    InvalidGameID,
    InvalidPosition,
)

# Expected response structure (shape name will be determined at test time)
expected_placement_response = GameStateResponse(
    game_id="1111-2222-3333-4444",
    grid=[
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, "#f0a000", 0, 0],
        [0, 0, 0, "#f0a000", "#f0a000", "#f0a000", 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    score=0,
    shape=[
        BlockBlastShape(
            name="J",
            coordinates=[(0, 0), (0, 1), (1, 0), (2, 0)],
            color="#0000f0",
        ),
        BlockBlastShape(
            name="S",
            coordinates=[(0, 1), (0, 2), (1, 0), (1, 1)],
            color="#00f000",
        ),
    ],
    status=GameState.PLAYER_TURN,
    game_over=False,
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


def test_place_shape_invalid_position(test_game_session_started) -> None:
    game = GameService()
    game.games["1111-2222-3333-4444"] = test_game_session_started

    # Valid game id and shape index, but the position is off the board.
    with pytest.raises(InvalidPosition, match="Cannot place"):
        game.place_shape("1111-2222-3333-4444", 0, 10, 10)
