from backend.src.game.constants import SHAPES
from backend.src.game.shapes import ShapeManager
from backend.src.models.shape import BlockBlastShape


# Hardcoded shapes to avoid flaky tests
SHAPE_I = BlockBlastShape("I", [(0, 0), (0, 1), (0, 2), (0, 3)], "#00f0f0")
SHAPE_O = BlockBlastShape("O", [(0, 0), (0, 1), (1, 0), (1, 1)], "#f0f000")
SHAPE_T = BlockBlastShape("T", [(0, 0), (0, 1), (0, 2), (1, 1)], "#a000f0")


def test_init() -> None:
    manager = ShapeManager(SHAPES)
    assert manager.available_shapes == SHAPES
    assert manager.current_shapes == []


def test_generate_new_set() -> None:
    manager = ShapeManager(
        {SHAPE_I.name: SHAPE_I, SHAPE_O.name: SHAPE_O, SHAPE_T.name: SHAPE_T}
    )
    shapes = manager.generate_new_set()
    assert len(shapes) == 3
    assert len(manager.current_shapes) == 3


def test_remove_shape() -> None:
    manager = ShapeManager(
        {SHAPE_I.name: SHAPE_I, SHAPE_O.name: SHAPE_O, SHAPE_T.name: SHAPE_T}
    )
    manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    manager.remove_shape(SHAPE_I)
    assert len(manager.current_shapes) == 2


def test_has_shapes() -> None:
    manager = ShapeManager({SHAPE_I.name: SHAPE_I})
    assert manager.has_shapes() is False
    manager.current_shapes = [SHAPE_I]
    assert manager.has_shapes() is True


def test_get_current_shapes() -> None:
    manager = ShapeManager(
        {SHAPE_I.name: SHAPE_I, SHAPE_O.name: SHAPE_O, SHAPE_T.name: SHAPE_T}
    )
    manager.current_shapes = [SHAPE_I, SHAPE_O, SHAPE_T]
    shapes = manager.get_current_shapes()
    assert len(shapes) == 3
