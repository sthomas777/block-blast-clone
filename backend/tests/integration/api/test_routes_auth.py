from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from backend.src.api.routes_auth import get_repo
from backend.src.main import app
from backend.src.models.player import Player
from backend.src.services.auth_service import ALGORITHM, hash_password, settings


@dataclass
class FakePlayerRepository:
    _by_id: dict[int, Player] = field(default_factory=dict)
    _next_id: int = 1

    def _add(self, username: str, hashed_password: str) -> Player:
        player = Player(username=username, hashed_password=hashed_password)
        player.player_id = self._next_id
        self._next_id += 1
        self._by_id[player.player_id] = player
        return player

    def seed(self, username: str, password: str) -> Player:
        return self._add(username, hash_password(password))

    async def create(self, username: str, hashed_password: str) -> Player:
        return self._add(username, hashed_password)

    async def get_by_username(self, username: str) -> Player | None:
        return next((p for p in self._by_id.values() if p.username == username), None)

    async def get_by_id(self, player_id: int) -> Player | None:
        return self._by_id.get(player_id)


@pytest.fixture
def repo() -> FakePlayerRepository:
    return FakePlayerRepository()


@pytest.fixture
def client(repo: FakePlayerRepository) -> Iterator[TestClient]:
    app.dependency_overrides[get_repo] = lambda: repo
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def _make_token(sub: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    payload = {"sub": sub, "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=ALGORITHM,
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
    token = _make_token(str(player.player_id))
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
    token = _make_token("123")
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_me_with_expired_token_returns_401(
    client: TestClient,
    repo: FakePlayerRepository,
) -> None:
    player = repo.seed("test", "supersecret")
    token = _make_token(str(player.player_id), expires_delta=timedelta(minutes=-1))
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_with_malformed_sub_returns_401(client: TestClient) -> None:
    token = _make_token("not-an-int")
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_without_token_returns_401(client: TestClient) -> None:
    response = client.get("/api/auth/me")
    assert response.status_code == 401
