from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.api import ws_game
from src.core.dependencies import game_service as shared_game_service
from src.game.session import GameState
from src.schemas.game import GameStateResponse
from src.services.game_service import GameService
from tests.integration.api._auth_helpers import FakeScoreRepository, make_token


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


def _patch_game_over(
    monkeypatch: pytest.MonkeyPatch,
    game_id: str,
    score: int,
) -> None:
    """Force dispatch to report game-over and seed a matching session."""
    session = MagicMock()
    session.state = GameState.GAME_OVER
    session.get_score.return_value = score
    shared_game_service.games[game_id] = session

    def fake_dispatch(
        raw: dict,
        gid: str | None,
        service: GameService,
    ) -> GameStateResponse:
        return GameStateResponse(
            game_id=game_id,
            status=GameState.GAME_OVER,
            grid=[[0] * 8 for _ in range(8)],
            score=score,
            shape=[],
            game_over=True,
        )

    monkeypatch.setattr(ws_game, "dispatch", fake_dispatch)


def test_game_over_saves_score_for_authenticated_player(
    client: TestClient,
    repo,
    score_repo: FakeScoreRepository,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    player = repo.seed("test", "supersecret")
    token = make_token(str(player.player_id))
    _patch_game_over(monkeypatch, "ws-auth-game", score=120)

    with client.websocket_connect(f"/ws/game?token={token}") as ws:
        ws.send_json({"command_type": "new_game"})
        assert ws.receive_json()["game_over"] is True

    saved = score_repo._scores
    assert len(saved) == 1
    assert saved[0].player_id == player.player_id
    assert saved[0].score == 120
    assert saved[0].lines_cleared == 12  # 120 // 10
    assert "ws-auth-game" not in shared_game_service.games  # cleaned up


def test_game_over_anonymous_cleans_up_without_saving(
    client: TestClient,
    score_repo: FakeScoreRepository,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_game_over(monkeypatch, "ws-anon-game", score=50)

    with client.websocket_connect("/ws/game") as ws:  # no token
        ws.send_json({"command_type": "new_game"})
        assert ws.receive_json()["game_over"] is True

    assert score_repo._scores == []
    assert "ws-anon-game" not in shared_game_service.games  # still cleaned up
