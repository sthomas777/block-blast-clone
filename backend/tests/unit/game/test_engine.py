from backend.src.game.board import GameBoard
from backend.src.game.constants import SHAPES
from backend.src.game.engine import GameEngine
from backend.src.game.scoring import ScoringEngine
from backend.src.game.shapes import ShapeManager
from backend.src.models.shape import BlockBlastShape


# Hardcoded shapes to avoid flaky tests
SHAPE_I = BlockBlastShape("I", [(0, 0), (0, 1), (0, 2), (0, 3)], "#00f0f0")
SHAPE_O = BlockBlastShape("O", [(0, 0), (0, 1), (1, 0), (1, 1)], "#f0f000")
SHAPE_T = BlockBlastShape("T", [(0, 0), (0, 1), (0, 2), (1, 1)], "#a000f0")


def test_init() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager(SHAPES)
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    assert engine.board == board
    assert engine.shape_manager == shape_manager
    assert engine.scoring == scoring


def test_can_place_shape() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager(SHAPES)
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    assert engine.can_place_shape(SHAPE_I, (0, 0)) is True


def test_place_shape() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager(
        {SHAPE_I.name: SHAPE_I, SHAPE_O.name: SHAPE_O, SHAPE_T.name: SHAPE_T},
    )
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    shape_manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    engine.place_shape(SHAPE_I, (0, 0))
    assert len(shape_manager.current_shapes) == 2
    assert SHAPE_I not in shape_manager.current_shapes


def test_process_board() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager(
        {SHAPE_I.name: SHAPE_I, SHAPE_O.name: SHAPE_O, SHAPE_T.name: SHAPE_T},
    )
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    shape_manager.current_shapes = []
    engine.process_board()
    assert len(shape_manager.current_shapes) == 3


def test_has_valid_moves() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager({SHAPE_I.name: SHAPE_I})
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    shape_manager.current_shapes = [SHAPE_I]
    assert engine.has_valid_moves() is True


def test_has_valid_moves_returns_false_when_board_full() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager({SHAPE_I.name: SHAPE_I})
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    shape_manager.current_shapes = [SHAPE_I]
    # Fill every cell so no shape can be placed anywhere.
    for r in range(board.rows):
        for c in range(board.cols):
            board.board[r, c] = "#ffffff"
    assert engine.has_valid_moves() is False


def test_get_score() -> None:
    board = GameBoard(rows=8, cols=8)
    shape_manager = ShapeManager(SHAPES)
    scoring = ScoringEngine()
    engine = GameEngine(board, shape_manager, scoring)
    scoring.add_lines_cleared(2)
    assert engine.get_score() == 20
