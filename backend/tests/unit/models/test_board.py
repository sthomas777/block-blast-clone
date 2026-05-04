from backend.src.models.board import BlockBlastBoard


def test_create_grid() -> None:
    grid = BlockBlastBoard(8, 8)
    assert len(grid.grid) == 8, "Board should have exactly 8 rows"

    assert all(len(row) == 8 for row in grid.grid), "Every row should have 8 columns"

    expected_grid = [[0 for _ in range(8)] for _ in range(8)]
    assert grid.grid == expected_grid, "Board should be initialized with all zeros"


def test__contains__() -> None:
    grid = BlockBlastBoard(8, 8)
    assert (1, 1) in grid


def test__getitem__() -> None:
    grid = BlockBlastBoard(8, 8)
    assert grid[1, 2] == 0
    assert grid[9, 9] == "OUT_OF_BOUND"


def test__setitem__() -> None:
    grid = BlockBlastBoard(8, 8)
    grid[2, 3] = "colour"
    assert grid[2, 3] == "colour"
