import pytest

from backend.src.game.constants import SHAPES
from backend.src.models.board import BlockBlastBoard
from backend.src.game.logic import place_shape, can_place_shape, clear_lines


def test_place_shape() -> None:
    grid = BlockBlastBoard(8, 8)
    place_shape(grid, SHAPES["O_0"], (5, 5))

    assert grid[5, 5] == 1, "Square is not place correctly at (5,5)"
    assert grid[5, 6] == 1, "Square is not place correctly at (5,6)"
    assert grid[6, 5] == 1, "Square is not place correctly at (6,5)"
    assert grid[6, 6] == 1, "Square is not place correctly at (6,6)"


def test_clear_lines() -> None:
    grid = BlockBlastBoard(8, 8)

    place_shape(grid, SHAPES["O_0"], (0, 0))
    place_shape(grid, SHAPES["O_0"], (2, 0))
    place_shape(grid, SHAPES["O_0"], (4, 0))
    place_shape(grid, SHAPES["O_0"], (6, 0))

    place_shape(grid, SHAPES["T_2"], (3, 5))

    no_lines = clear_lines(grid)

    assert no_lines == 2, "Square is not clear correctly"
    assert grid[0] == [0, 0, 0, 0, 0, 0, 0, 0]
    assert grid[1] == [0, 0, 0, 0, 0, 0, 0, 0]


def test_can_place_shape() -> None:
    grid = BlockBlastBoard(8, 8)

    place_shape(grid, SHAPES["O_0"], (0, 0))
    place_shape(grid, SHAPES["O_0"], (2, 0))
    place_shape(grid, SHAPES["O_0"], (4, 0))
    place_shape(grid, SHAPES["O_0"], (6, 0))

    cannot_place = can_place_shape(grid, SHAPES["I_1"], (2, 0))

    assert grid[2, 0] != 0, "Shape is not place correctly at (2,0)"
    assert cannot_place is False, "Shape is not place correctly at (2,0)"

    out_of_bound = can_place_shape(grid, SHAPES["I_1"], (8, 8))
    with pytest.raises(IndexError):
        grid[SHAPES["I_1"].coordinates[0][0] + 8, SHAPES["I_1"].coordinates[1][0] + 8]

    assert out_of_bound is False, "Shape is not place correctly at (8,8)"

    in_bound = can_place_shape(grid, SHAPES["I_1"], (4, 3))
    assert in_bound is True, "Shape is not place correctly at (4,3)"
