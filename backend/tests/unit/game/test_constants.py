import pytest

from backend.src.game.constants import (
    COL_GRID_SIZE,
    ROW_GRID_SIZE,
    BASE_SHAPES,
    generate_library,
    SHAPES,
)
from backend.src.models.shape import BlockBlastShape


def test_grid_size() -> None:
    assert COL_GRID_SIZE == 8
    assert ROW_GRID_SIZE == 8


@pytest.mark.parametrize(
    "index,expected",
    [
        pytest.param(
            0,
            BlockBlastShape("I", [(0, 0), (0, 1), (0, 2), (0, 3)], "#00f0f0"),
        ),
        pytest.param(
            1,
            BlockBlastShape("O", [(0, 0), (0, 1), (1, 0), (1, 1)], "#f0f000"),
        ),
        pytest.param(
            2,
            BlockBlastShape("T", [(0, 0), (0, 1), (0, 2), (1, 1)], "#a000f0"),
        ),
        pytest.param(
            3,
            BlockBlastShape("L", [(0, 0), (1, 0), (2, 0), (2, 1)], "#f0a000"),
        ),
        pytest.param(
            4, BlockBlastShape("J", [(0, 1), (1, 1), (2, 1), (2, 0)], "#0000f0")
        ),
        pytest.param(
            6,
            BlockBlastShape("Z", [(0, 0), (0, 1), (1, 1), (1, 2)], "#f00000"),
        ),
    ],
)
def test_base_shape(index: int, expected: BlockBlastShape) -> None:
    assert isinstance(BASE_SHAPES[index], BlockBlastShape)
    assert BASE_SHAPES[index] == expected


def test_generate_library() -> None:
    assert len(generate_library(BASE_SHAPES)) == len(SHAPES)

    i_shape = [BASE_SHAPES[0]]
    generated_shape = generate_library(i_shape)
    assert len(generated_shape) == 2
    assert generated_shape["I_0"].coordinates == [(0, 0), (0, 1), (0, 2), (0, 3)]
    assert generated_shape["I_1"].coordinates == [(0, 0), (1, 0), (2, 0), (3, 0)]
