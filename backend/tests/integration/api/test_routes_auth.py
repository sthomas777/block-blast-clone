from datetime import timedelta

from fastapi.testclient import TestClient

from backend.tests.integration.api._auth_helpers import (
    FakePlayerRepository,
    make_token,
)


def test_register_returns_player(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={"username": "test", "password": "supersecret"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "test"
    assert "player_id" in body


def test_register_duplicate_username_returns_409(
    client: TestClient,
    repo: FakePlayerRepository,
) -> None:
    repo.seed("test", "supersecret")
    response = client.post(
        "/api/auth/register",
        json={"username": "test", "password": "anothersecret"},
    )
    assert response.status_code == 409


def test_token_with_valid_credentials_returns_token(
    client: TestClient,
    repo: FakePlayerRepository,
) -> None:
    repo.seed("test", "supersecret")
    response = client.post(
        "/api/auth/token",
        data={"username": "test", "password": "supersecret"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_token_with_bad_password_returns_401(
    client: TestClient,
    repo: FakePlayerRepository,
) -> None:
    repo.seed("test", "supersecret")
    response = client.post(
        "/api/auth/token",
        data={"username": "test", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_token_unknown_user_returns_401(client: TestClient) -> None:
    response = client.post(
        "/api/auth/token",
        data={"username": "test", "password": "supersecret"},
    )
    assert response.status_code == 401


def test_me_with_valid_token_returns_200(
    client: TestClient,
    repo: FakePlayerRepository,
) -> None:
    player = repo.seed("test", "supersecret")
    token = make_token(str(player.player_id))
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "test"


def test_me_with_invalid_token_returns_401(client: TestClient) -> None:
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert response.status_code == 401


def test_me_with_valid_token_but_missing_player_returns_404(client: TestClient) -> None:
    # Well-signed token whose player_id no longer exists in the repo.
    token = make_token("123")
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_me_with_expired_token_returns_401(
    client: TestClient,
    repo: FakePlayerRepository,
) -> None:
    player = repo.seed("test", "supersecret")
    token = make_token(str(player.player_id), expires_delta=timedelta(minutes=-1))
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_with_malformed_sub_returns_401(client: TestClient) -> None:
    token = make_token("not-an-int")
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_without_token_returns_401(client: TestClient) -> None:
    response = client.get("/api/auth/me")
    assert response.status_code == 401
