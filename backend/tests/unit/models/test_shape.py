from backend.src.models.shape import BlockBlastShape


def test_shape_model() -> None:
    shape = BlockBlastShape(
        name="Block Name",
        coordinates=[(0, 0)],
        color="skyblue",
    )
    assert shape.name == "Block Name"
    assert shape.coordinates == [(0, 0)]
    assert shape.color == "skyblue"


def test_shape_rotate() -> None:
    shape = BlockBlastShape(
        name="Block Name",
        coordinates=[(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 3)],
        color="skyblue",
    )
    rotated = shape.rotate()
    assert rotated.name == "Block Name"
    assert rotated.coordinates == [(0, 3), (1, 3), (2, 1), (2, 2), (2, 3), (3, 0)]
    assert rotated.color == "skyblue"
