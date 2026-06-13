from fastapi.testclient import TestClient

from tests.integration.api._auth_helpers import (
    FakePlayerRepository,
    FakeScoreRepository,
    make_token,
)


def test_get_my_scores_returns_player_scores(
    client: TestClient,
    repo: FakePlayerRepository,
    score_repo: FakeScoreRepository,
) -> None:
    player = repo.seed("test", "supersecret")
    score_repo.seed(player.player_id, 100)
    score_repo.seed(player.player_id, 300)
    token = make_token(str(player.player_id))

    response = client.get(
        "/api/scores/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert [s["score"] for s in body] == [300, 100]
    assert all(s["player_id"] == player.player_id for s in body)


def test_get_my_scores_requires_auth(client: TestClient) -> None:
    # Same shared dependency as /me, so an unauthenticated request is rejected.
    response = client.get("/api/scores/me")
    assert response.status_code == 401


def test_get_my_scores_missing_player_returns_404(
    client: TestClient,
) -> None:
    # Valid token but the player does not exist -> get_authenticated_player 404s.
    token = make_token("123")
    response = client.get(
        "/api/scores/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
