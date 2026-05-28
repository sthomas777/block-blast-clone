import pytest
from backend.src.services.game_service import GameService, InvalidGameID
from backend.tests.unit.services.data.test_get_game_data import expected_game

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


def test_get_game(test_game_session) -> None:
    game = GameService()
    game.games["1111-2222-3333-4444"] = test_game_session

    actual = game.get_game("1111-2222-3333-4444")

    assert actual == expected_game


def test_get_game_invalid_game_id() -> None:
    """Test that get_game raises InvalidGameID for non-existent game"""
    game = GameService()

    with pytest.raises(InvalidGameID, match="Invalid game id"):
        game.get_game("non-existent-id")


def test_get_game_empty_string_id() -> None:
    """Test that get_game raises InvalidGameID for empty string"""
    game = GameService()

    with pytest.raises(InvalidGameID):
        game.get_game("")
