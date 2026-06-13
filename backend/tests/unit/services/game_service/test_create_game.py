from src.game.session import GameState
from src.services.game_service import GameService

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


def test_create_game() -> None:
    game = GameService()
    session = game.create_game()

    assert len(session.game_id) == 36
    assert session.game_over is False
    assert session.grid == EMPTY_GRID
    assert session.score == 0
    assert len(session.shape) == 3
    assert session.status == GameState.PLAYER_TURN


def test_create_multiple_games() -> None:
    """Test that multiple games can be created with unique IDs"""
    game = GameService()

    game1 = game.create_game()
    game2 = game.create_game()

    assert game1.game_id != game2.game_id
    assert len(game.games) == 2
    assert game1.game_id in game.games
    assert game2.game_id in game.games


def test_create_game_returns_valid_response() -> None:
    """Test that create_game returns GameStateResponse with correct structure"""
    game = GameService()

    response = game.create_game()

    assert len(response.game_id) == 36
    assert response.status == GameState.PLAYER_TURN
    assert response.grid == EMPTY_GRID
    assert response.score == 0
    assert len(response.shape) == 3
    assert response.game_over is False
