from fastapi.testclient import TestClient

from backend.src.game.session import GameState
from backend.src.schemas.game import (
    GameStateResponse,
    PlaceShapeRequest,
    GameStateMLResponse,
)

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


def test_new_game(game_fixture: GameStateResponse) -> None:
    assert len(game_fixture.game_id) == 36
    assert game_fixture.game_over is False
    assert game_fixture.grid == EMPTY_GRID
    assert game_fixture.score == 0
    assert len(game_fixture.shape) == 3
    assert game_fixture.status == GameState.PLAYER_TURN


def test_get_game(client: TestClient, game_fixture: GameStateResponse) -> None:
    response = client.get(f"/game/{game_fixture.game_id}")
    assert response.status_code == 200
    game = GameStateResponse(**response.json())
    assert game.game_id == game_fixture.game_id


def test_get_game_fake_id(client: TestClient) -> None:
    response = client.get("/game/aasdfasdf")
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid game id"


def test_place_shape(client: TestClient, game_fixture: GameStateResponse) -> None:
    test_data = dict(
        PlaceShapeRequest(
            shape_index=0,
            row=3,
            col=3,
        ),
    )
    response = client.post(f"/game/{game_fixture.game_id}/place", json=test_data)
    assert response.status_code == 200

    game = GameStateResponse(**response.json())
    assert game.game_id == game_fixture.game_id
    assert game.status == GameState.PLAYER_TURN
    assert game.score == 0


def test_place_shape_fake_id(client: TestClient) -> None:
    test_data = dict(
        PlaceShapeRequest(
            shape_index=0,
            row=3,
            col=3,
        ),
    )
    response = client.post("/game/asdfasdfasdf/place", json=test_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid game id. Not in list of game ids"


def test_place_shape_invalid_placement(
    client: TestClient,
    game_fixture: GameStateResponse,
) -> None:
    test_data = dict(
        PlaceShapeRequest(
            shape_index=0,
            row=7,
            col=7,
        ),
    )
    response = client.post(f"/game/{game_fixture.game_id}/place", json=test_data)

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == f"Cannot place {game_fixture.shape[0].name} at position (7, 7)"
    )


def test_get_ml_state(client: TestClient, game_fixture: GameStateResponse) -> None:
    response = client.get(f"/game/{game_fixture.game_id}/ml_state")
    assert response.status_code == 200

    game = GameStateMLResponse(**response.json())
    assert game.game_over is False
    assert len(game.shape) == 3
    assert game.score == 0
    assert game.grid == EMPTY_GRID
