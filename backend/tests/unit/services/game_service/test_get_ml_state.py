import pytest
from backend.src.schemas.game import GameStateMLResponse
from backend.src.services.game_service import GameService, InvalidGameID

EMPTY_GRID = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

expected_game = GameStateMLResponse(
    grid=EMPTY_GRID,
    score=0,
    shape=[],
    game_over=False,
)


def test_get_ml_state(test_game_session) -> None:
    game = GameService()
    game.games["1111-2222-3333-4444"] = test_game_session

    actual = game.get_ml_state("1111-2222-3333-4444")

    assert actual == expected_game


def test_get_ml_state_invalid_game_id() -> None:
    """Test that get_ml_state raises InvalidGameID for non-existent game"""
    game = GameService()

    with pytest.raises(InvalidGameID, match="Invalid game id"):
        game.get_ml_state("non-existent-id")


def test_get_ml_state_valid_game(test_game_session) -> None:
    """Test that get_ml_state returns GameStateMLResponse with correct structure"""
    game = GameService()
    game.games["1111-2222-3333-4444"] = test_game_session

    ml_state = game.get_ml_state("1111-2222-3333-4444")

    assert ml_state.grid == EMPTY_GRID
    assert ml_state.score == 0
    assert ml_state.shape == []
    assert ml_state.game_over is False
