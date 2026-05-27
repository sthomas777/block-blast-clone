from dataclasses import dataclass, field
from uuid import uuid4
from backend.src.game.session import GameSession, GameState


@dataclass
class GameService:
    games: dict[str, GameSession] = field(default_factory=dict)

    def create_game(self) -> dict[str, str | GameState]:
        game_id = str(uuid4())
        session = GameSession(board_size=(8, 8))
        session.start()
        self.games[game_id] = session
        return {"game_id": game_id, "state": session.state}

    def get_game(self, game_id: str) -> dict[str, str | GameState]:
        return {"game_id": game_id, "state": self.games[game_id].state}

    def place_block(self, game_id: str) -> dict:
        session = self.games[game_id]
        session.confirm_placement()
        return {"game_id": game_id, "state": session.state}
