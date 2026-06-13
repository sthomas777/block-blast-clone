from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from src.core.dependencies import get_repo, get_score_repo
from src.main import app
from tests.integration.api._auth_helpers import (
    FakePlayerRepository,
    FakeScoreRepository,
)


@pytest.fixture
def repo() -> FakePlayerRepository:
    return FakePlayerRepository()


@pytest.fixture
def score_repo() -> FakeScoreRepository:
    return FakeScoreRepository()


@pytest.fixture
def client(
    repo: FakePlayerRepository,
    score_repo: FakeScoreRepository,
) -> Iterator[TestClient]:
    app.dependency_overrides[get_repo] = lambda: repo
    app.dependency_overrides[get_score_repo] = lambda: score_repo
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
