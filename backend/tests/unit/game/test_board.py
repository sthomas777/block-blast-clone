from backend.src.game.board import GameBoard


def test_init() -> None:
    board = GameBoard(rows=8, cols=8)
    assert board.rows == 8
    assert board.cols == 8
    assert len(board.grid) == 8
    assert len(board.grid[0]) == 8


def test_can_place_at_valid() -> None:
    board = GameBoard(rows=8, cols=8)
    coords = [(0, 0), (0, 1)]
    assert board.can_place_at(coords, (0, 0)) is True


def test_can_place_at_out_of_bounds() -> None:
    board = GameBoard(rows=8, cols=8)
    coords = [(0, 0), (0, 1)]
    assert board.can_place_at(coords, (7, 7)) is False


def test_place_shape() -> None:
    board = GameBoard(rows=8, cols=8)
    coords = [(0, 0), (0, 1)]
    board.place_shape(coords, (0, 0))
    assert board.grid[0][0] == 1
    assert board.grid[0][1] == 1


def test_clear_lines_no_lines() -> None:
    board = GameBoard(rows=8, cols=8)
    cleared = board.clear_lines()
    assert cleared == 0


def test_clear_lines_full_row():
    board = GameBoard(rows=8, cols=8)
    board.board[0] = [1] * 8
    cleared = board.clear_lines()
    assert cleared == 1
    assert board.grid[0] == [0] * 8


def test_clear_lines_full_column() -> None:
    board = GameBoard(rows=8, cols=8)
    for r in range(8):
        board.board[r, 0] = 1
    cleared = board.clear_lines()
    assert cleared == 1
    for r in range(8):
        assert board.board[r, 0] == 0
