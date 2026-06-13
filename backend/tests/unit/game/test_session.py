from src.game.session import GameSession
from src.models.shape import BlockBlastShape
from src.game.board import GameBoard
from src.game.shapes import ShapeManager
from src.game.scoring import ScoringEngine
from src.game.engine import GameEngine


# Hardcoded shapes to avoid flaky tests
SHAPE_I = BlockBlastShape("I", [(0, 0), (0, 1), (0, 2), (0, 3)], "#00f0f0")
SHAPE_O = BlockBlastShape("O", [(0, 0), (0, 1), (1, 0), (1, 1)], "#f0f000")
SHAPE_T = BlockBlastShape("T", [(0, 0), (0, 1), (0, 2), (1, 1)], "#a000f0")


def test_init() -> None:
    session = GameSession(board_size=(8, 8))
    assert session.board_size == (8, 8)
    assert session.state.name == "START"
    assert session.engine is not None


def test_start() -> None:
    session = GameSession(board_size=(8, 8))
    session.start()
    assert session.state.name == "PLAYER_TURN"
    assert len(session.get_available_shapes()) == 3


def test_preview_shape() -> None:
    session = GameSession(board_size=(8, 8))
    session.start()
    session.engine.shape_manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    result = session.preview_shape(SHAPE_I, (0, 0))
    assert result is True
    assert session.state.name == "SHAPE_PREVIEW"


def test_preview_shape_invalid() -> None:
    session = GameSession(board_size=(8, 8))
    session.start()
    session.engine.shape_manager.current_shapes = [SHAPE_I]
    result = session.preview_shape(SHAPE_I, (10, 10))
    assert result is False


def test_confirm_placement() -> None:
    session = GameSession(board_size=(8, 8))
    session.start()
    session.engine.shape_manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    session.preview_shape(SHAPE_I, (0, 0))
    session.confirm_placement()
    assert session.state.name == "PLAYER_TURN"


def test_confirm_placement_game_over_when_no_moves_left(monkeypatch) -> None:
    session = GameSession(board_size=(8, 8))
    session.start()
    session.engine.shape_manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    scores: list[int] = []
    session.on("game_over", scores.append)

    session.preview_shape(SHAPE_I, (0, 0))
    # Force the "no valid moves remain" branch after the placement.
    monkeypatch.setattr(session.engine, "has_valid_moves", lambda: False)
    session.confirm_placement()

    assert session.state.name == "GAME_OVER"
    assert session.is_game_over() is True
    assert len(scores) == 1


def test_is_game_over() -> None:
    session = GameSession(board_size=(8, 8))
    assert session.is_game_over() is False


def test_get_score() -> None:
    session = GameSession(board_size=(8, 8))
    assert session.get_score() == 0


def test_get_available_shapes() -> None:
    session = GameSession(board_size=(8, 8))
    session.start()
    shapes = session.get_available_shapes()
    assert len(shapes) == 3


def test_get_board_grid() -> None:
    session = GameSession(board_size=(8, 8))
    grid = session.get_board_grid()
    assert len(grid) == 8
    assert len(grid[0]) == 8


def test_event_listeners():
    session = GameSession(board_size=(8, 8))
    called = []
    session.on("shape_placed", lambda *args: called.append("placed"))
    session.start()
    session.engine.shape_manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    session.preview_shape(SHAPE_I, (0, 0))
    session.confirm_placement()
    assert "placed" in called


def test_game_over_event() -> None:
    session = GameSession(board_size=(6, 6))
    called = []
    session.on("game_over", lambda score: called.append(score))
    # Directly test the emit by checking listeners work
    session.emit("game_over", 100)
    assert len(called) == 1
    assert called[0] == 100


def test_place_current_shape_none() -> None:
    from src.game.session import GameContext, place_current_shape

    board = GameBoard(rows=6, cols=6)
    shape_manager = ShapeManager({SHAPE_I.name: SHAPE_I})
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    context = GameContext(engine=engine, current_shape=None)
    place_current_shape(context)
    assert context.current_shape is None
