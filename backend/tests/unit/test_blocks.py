from src.game.blocks import BLOCKS


def test_blocks_names() -> None:
    assert list(BLOCKS.keys()) == [
        "single_cell",
        "square",
        "horizontal_line",
        "vertical_line",
        "l_shape",
        "t_shape",
    ]


def test_blocks_values() -> None:
    assert list(BLOCKS.values()) == [
        [(0, 0)],  # single_cell
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # square
        [(0, 0), (0, 1), (0, 2)],  # horizontal_line
        [(0, 0), (1, 0), (2, 0)],  # vertical_line
        [(0, 0), (1, 0), (2, 0), (2, 1)],  # l_shape
        [(0, 0), (1, 0), (2, 0), (1, 1)],  # t_shape
    ]


def test_starting_point_of_blocks() -> None:
    starting_point_of_blocks = [starting_point[0] for starting_point in BLOCKS.values()]
    for sp in starting_point_of_blocks:
        assert sp == (0, 0)
