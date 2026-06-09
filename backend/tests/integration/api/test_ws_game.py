import pytest
from fastapi.testclient import TestClient

from backend.src.api import ws_game
from backend.src.services.game_service import GameService


def test_new_game_returns_state(client: TestClient) -> None:
    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"command_type": "new_game"})
        state = ws.receive_json()

    assert len(state["game_id"]) == 36
    assert state["game_over"] is False
    assert len(state["shape"]) == 3
    assert state["score"] == 0
    assert len(state["grid"]) == 8


def test_place_shape_after_new_game(client: TestClient) -> None:
    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"command_type": "new_game"})
        created = ws.receive_json()

        ws.send_json(
            {"command_type": "place_shape", "shape_index": 0, "row": 3, "col": 3},
        )
        updated = ws.receive_json()

    assert updated["game_id"] == created["game_id"]
    assert updated["status"] == created["status"]
    assert (
        len(updated["shape"]) == len(created["shape"]) - 1
    )  # Making it explicitly clear that we have 1 less shape


def test_place_shape_before_new_game_is_game_error(client: TestClient) -> None:
    with client.websocket_connect("/ws/game") as ws:
        ws.send_json(
            {"command_type": "place_shape", "shape_index": 0, "row": 3, "col": 3},
        )
        error = ws.receive_json()

    assert error["command_type"] == "error"
    assert error["code"] == "game_error"


def test_unknown_type_is_validation_error(client: TestClient) -> None:
    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"command_type": "nonsense"})
        error = ws.receive_json()

    assert error["code"] == "validation_error"


def test_out_of_range_field_is_validation_error(client: TestClient) -> None:
    with client.websocket_connect("/ws/game") as ws:
        ws.send_json(
            {"command_type": "place_shape", "shape_index": 9, "row": 3, "col": 3},
        )
        error = ws.receive_json()

    assert error["code"] == "validation_error"


def test_socket_survives_error_and_keeps_serving(client: TestClient) -> None:
    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"command_type": "nonsense"})
        assert ws.receive_json()["code"] == "validation_error"

        ws.send_json({"command_type": "new_game"})
        assert len(ws.receive_json()["game_id"]) == 36


def test_unexpected_error_returns_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unexpected (non-validation, non-game) error is reported generically."""

    def boom(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("unexpected failure")

    monkeypatch.setattr(ws_game, "dispatch", boom)

    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"command_type": "new_game"})
        error = ws.receive_json()

    assert error["code"] == "internal_error"
    assert error["message"] == "Internal server error"


def test_socket_survives_unexpected_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unexpected error must not close the socket — the next message works."""
    real_dispatch = ws_game.dispatch
    calls = {"count": 0}

    def flaky(raw: dict, game_id: str | None, service: GameService) -> object:
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("unexpected failure")
        return real_dispatch(raw, game_id, service)

    monkeypatch.setattr(ws_game, "dispatch", flaky)

    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"command_type": "new_game"})
        assert ws.receive_json()["code"] == "internal_error"

        ws.send_json({"command_type": "new_game"})
        assert len(ws.receive_json()["game_id"]) == 36
