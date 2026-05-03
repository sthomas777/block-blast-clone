import pytest
from src.game.board import Board


def test_create_grid() -> None:
    grid = Board()
    assert len(grid.grid) == 8, "Board should have exactly 8 rows"

    assert all(len(row) == 8 for row in grid.grid), "Every row should have 8 columns"

    expected_grid = [[0 for _ in range(8)] for _ in range(8)]
    assert grid.grid == expected_grid, "Board should be initialized with all zeros"


def test_print_grid(capsys: pytest.CaptureFixture[str]) -> None:
    grid = Board()
    grid.print_grid()
    captured = capsys.readouterr()
    expected_output = (
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
    )

    assert expected_output == captured.out


@pytest.mark.parametrize(
    "shape, row, col, expected, reason",
    [
        ("square", 4, 4, False, "Should not place on occupied cells"),
        ("square", 9, 0, False, "Should fail when row > 7"),
        ("square", 0, 9, False, "Should fail when col > 7"),
        ("square", -1, 4, False, "Should fail when row < 0"),
        ("square", 0, -4, False, "Should fail when col < 0"),
        ("square", 2, 2, True, "Should succeed on empty, in-bounds valid position"),
        (
            "square",
            7,
            7,
            False,
            "Should fail if shape dimensions exceed board boundaries",
        ),
    ],
)
def test_can_place(shape: str, row: int, col: int, expected: bool, reason: str) -> None:
    grid = Board()
    grid.grid[4][4] = 1
    grid.grid[5][5] = 1

    assert grid.can_place(shape, row, col) is expected, (
        f"Failed: {reason} ({shape} at {row}, {col})"
    )


def test_place_shape(capsys: pytest.CaptureFixture[str]) -> None:
    grid = Board()
    grid.place_shape("square", 5, 5)
    grid.print_grid()
    captured = capsys.readouterr()
    assert grid.grid[5][5] == 1, "Square is not place correctly at (5,5)"
    assert grid.grid[5][6] == 1, "Square is not place correctly at (5,6)"
    assert grid.grid[6][5] == 1, "Square is not place correctly at (6,5)"
    assert grid.grid[6][6] == 1, "Square is not place correctly at (6,6)"
    expected_output = (
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 1 1 0\n"
        "0 0 0 0 0 1 1 0\n"
        "0 0 0 0 0 0 0 0\n"
    )

    assert expected_output == captured.out, (
        "There are more shapes on board than intended"
    )


def test_clear_lines(capsys: pytest.CaptureFixture[str]) -> None:
    board = Board()
    board.place_shape("square", 6, 0)
    board.place_shape("square", 6, 2)
    board.place_shape("square", 6, 4)
    board.place_shape("square", 6, 6)
    board.place_shape("square", 4, 0)
    board.place_shape("square", 4, 4)
    board.place_shape("square", 4, 2)
    board.place_shape("square", 4, 4)
    board.place_shape("square", 2, 2)
    board.place_shape("horizontal_line", 0, 0)
    board.place_shape("vertical_line", 1, 0)

    expected_cleared_lines = board.clear_lines()
    assert expected_cleared_lines == 3, (
        "More/lines lines have been cleared than intended"
    )

    board.print_grid()
    captured = capsys.readouterr()
    expected_output = (
        "0 1 1 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 1 1 0 0 0 0\n"
        "0 0 1 1 0 0 0 0\n"
        "0 1 1 1 1 1 0 0\n"
        "0 1 1 1 1 1 0 0\n"
        "0 0 0 0 0 0 0 0\n"
        "0 0 0 0 0 0 0 0\n"
    )

    assert expected_output == captured.out, (
        "Either some lines have not been cleared or additional positions have been cleared"
    )


def test_get_grid() -> None:
    grid = Board()
    assert grid.get_grid() == grid.grid
