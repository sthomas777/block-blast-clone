from dataclasses import dataclass, field
from uuid import uuid4
from backend.src.game.session import GameSession
from backend.src.schemas.game import GameStateResponse, PlaceShapeResponse


@dataclass
class GameService:
    games: dict[str, GameSession] = field(default_factory=dict)

    def create_game(self) -> GameStateResponse:
        game_id = str(uuid4())
        session = GameSession(board_size=(8, 8))
        session.start()
        score = session.get_score()
        available_shapes = session.get_available_shapes()
        self.games[game_id] = session
        return GameStateResponse(
            game_id=game_id,
            status=session.state,
            grid=session.board,
            score=score,
            shape=available_shapes,
        )

    def get_game(self, game_id: str) -> GameStateResponse:
        game_session = self.games[game_id]
        game_session_score = game_session.get_score()
        game_session_available_shapes = game_session.get_available_shapes()
        return GameStateResponse(
            game_id=game_id,
            status=game_session.state,
            grid=game_session.board,
            score=game_session_score,
            shape=game_session_available_shapes,
        )

    def place_shape(
        self,
        game_id: str,
        shape_index: int,
        row: int,
        col: int,
    ) -> PlaceShapeResponse | None:
        session = self.games[game_id]
        shape = session.get_available_shapes()[shape_index]
        if not session.preview_shape(shape, (row, col)):
            return None
        session.confirm_placement()
        score = session.get_score()
        return PlaceShapeResponse(
            game_id=game_id,
            status=session.state,
            shape=shape.name,
            placement=(row, col),
            score=score,
        )
