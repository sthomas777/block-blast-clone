from typing import Iterator

import pytest

from backend.src.models.board import BlockBlastBoard


def test_create_grid() -> None:
    grid = BlockBlastBoard(8, 8)
    assert grid.rows == 8, "Board should have exactly 8 rows"
    assert grid.cols == 8, "Board should have exactly 8 columns"

    assert all(len(row) == grid.cols for row in grid), "Every row should have 8 columns"

    expected_grid = [[0 for _ in range(8)] for _ in range(8)]
    assert grid.grid == expected_grid, "Board should be initialized with all zeros"


def test__contains__() -> None:
    grid = BlockBlastBoard(8, 8)
    assert (1, 1) in grid


def test__getitem__() -> None:
    grid = BlockBlastBoard(8, 8)
    assert grid[1, 2] == 0

    assert grid[2] == [0, 0, 0, 0, 0, 0, 0, 0]
    with pytest.raises(IndexError):
        grid[9, 9]


def test__setitem__() -> None:
    grid = BlockBlastBoard(8, 8)
    grid[2, 3] = "colour"
    assert grid[2, 3] == "colour"

    grid[1] = [20] * 8
    assert grid[1] == [20, 20, 20, 20, 20, 20, 20, 20]


def test__iter__() -> None:
    grid = BlockBlastBoard(8, 8)
    assert isinstance(grid.__iter__(), Iterator)
