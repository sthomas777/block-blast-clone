import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.schemas.game import GameStateResponse


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def game_fixture(client: TestClient) -> GameStateResponse:
    """Create a game and return its ID — reusable fixture."""
    response = client.post("/game/new")
    assert response.status_code == 200

    return GameStateResponse(**response.json())
