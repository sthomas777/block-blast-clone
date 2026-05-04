from backend.src.game.constants import SHAPES
from backend.src.models.board import BlockBlastBoard
from backend.src.game.logic import BlockBlastLogic


def test_place_shape() -> None:
    grid = BlockBlastBoard(8, 8)
    logic = BlockBlastLogic()
    logic.place_shape(grid, SHAPES[2], (5, 5))

    assert grid[5, 5] == "#f0f000", "Square is not place correctly at (5,5)"
    assert grid[5, 6] == "#f0f000", "Square is not place correctly at (5,6)"
    assert grid[6, 5] == "#f0f000", "Square is not place correctly at (6,5)"
    assert grid[6, 6] == "#f0f000", "Square is not place correctly at (6,6)"


def test_clear_lines() -> None:
    pass


def test_can_place_shape() -> None:
    pass
