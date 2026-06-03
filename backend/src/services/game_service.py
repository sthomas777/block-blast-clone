from dataclasses import dataclass, field
from uuid import uuid4
from backend.src.game.session import GameSession
from backend.src.schemas.game import (
    GameStateResponse,
    GameStateMLResponse,
)


class InvalidPosition(Exception):
    pass


class InvalidGameID(Exception):
    pass


@dataclass
class GameService:
    games: dict[str, GameSession] = field(default_factory=dict)

    def create_game(self) -> GameStateResponse:
        game_id = str(uuid4())
        session = GameSession(board_size=(8, 8))
        session.start()
        score = session.get_score()
        game_over = session.is_game_over()
        available_shapes = session.get_available_shapes()
        self.games[game_id] = session
        return GameStateResponse(
            game_id=game_id,
            status=session.state,
            grid=session.board.grid,
            score=score,
            shape=available_shapes,
            game_over=game_over,
        )

    def get_game(self, game_id: str) -> GameStateResponse:
        if game_id not in self.games:
            raise InvalidGameID("Invalid game id")
        game_session = self.games[game_id]
        game_session_score = game_session.get_score()
        game_session_available_shapes = game_session.get_available_shapes()
        game_over = game_session.is_game_over()
        return GameStateResponse(
            game_id=game_id,
            status=game_session.state,
            grid=game_session.board.grid,
            score=game_session_score,
            shape=game_session_available_shapes,
            game_over=game_over,
        )

    def place_shape(
        self,
        game_id: str,
        shape_index: int,
        row: int,
        col: int,
    ) -> GameStateResponse:
        if game_id not in self.games:
            raise InvalidGameID("Invalid game id")
        session = self.games[game_id]
        if not (0 <= shape_index <= 2):
            raise InvalidPosition(
                f"Invalid shape has been chosen at position {shape_index}",
            )
        shape = session.get_available_shapes()[shape_index]
        if not session.preview_shape(shape, (row, col)):
            raise InvalidPosition(f"Cannot place {shape.name} at position {(row, col)}")
        session.confirm_placement()

        return GameStateResponse(
            game_id=game_id,
            status=session.state,
            grid=session.board.grid,
            score=session.get_score(),
            shape=session.get_available_shapes(),
            game_over=session.is_game_over(),
        )

    def get_ml_state(self, game_id: str) -> GameStateMLResponse:
        if game_id not in self.games:
            raise InvalidGameID("Invalid game id")
        session = self.games[game_id]
        game_board = session.board.grid
        game_over = session.is_game_over()
        game_score = session.get_score()
        available_shape = session.get_available_shapes()
        return GameStateMLResponse(
            grid=game_board,
            score=game_score,
            shape=available_shape,
            game_over=game_over,
        )
