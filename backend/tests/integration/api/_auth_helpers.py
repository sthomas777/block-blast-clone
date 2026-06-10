"""Shared test doubles and helpers for the API integration tests."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import jwt

from backend.src.models.player import Player
from backend.src.models.score import Score
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


@dataclass
class FakeScoreRepository:
    _scores: list[Score] = field(default_factory=list)

    def seed(self, player_id: int, score: int) -> Score:
        return self._add(
            player_id,
            session_id=1,
            score=score,
            lines_cleared=score // 10,
        )

    def _add(
        self,
        player_id: int,
        session_id: int | None,
        score: int,
        lines_cleared: int,
    ) -> Score:
        row = Score(
            player_id=player_id,
            session_id=session_id,
            score=score,
            lines_cleared=lines_cleared,
        )
        row.score_id = len(self._scores) + 1
        row.achieved_at = datetime.now(timezone.utc)
        self._scores.append(row)
        return row

    async def save_score(
        self,
        player_id: int,
        session_id: int | None,
        player_score: int,
        lines_cleared: int,
    ) -> Score:
        return self._add(player_id, session_id, player_score, lines_cleared)

    async def get_player_scores(self, player_id: int, limit: int = 10) -> list[Score]:
        owned = [s for s in self._scores if s.player_id == player_id]
        return sorted(owned, key=lambda s: s.score, reverse=True)[:limit]


def make_token(sub: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    payload = {"sub": sub, "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=ALGORITHM,
    )
