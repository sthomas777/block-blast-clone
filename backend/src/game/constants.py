from collections import defaultdict

from backend.src.models.shape import BlockBlastShape

BASE_SHAPES = [
    BlockBlastShape("I", [(0, 0), (0, 1), (0, 2), (0, 3)], "#00f0f0"),
    BlockBlastShape("O", [(0, 0), (0, 1), (1, 0), (1, 1)], "#f0f000"),
    BlockBlastShape("T", [(0, 0), (0, 1), (0, 2), (1, 1)], "#a000f0"),
    BlockBlastShape("L", [(0, 0), (1, 0), (2, 0), (2, 1)], "#f0a000"),
    BlockBlastShape("J", [(0, 1), (1, 1), (2, 1), (2, 0)], "#0000f0"),
    BlockBlastShape("S", [(0, 1), (0, 2), (1, 0), (1, 1)], "#00f000"),
    BlockBlastShape("Z", [(0, 0), (0, 1), (1, 1), (1, 2)], "#f00000"),
]


def generate_library(bases: list[BlockBlastShape]) -> dict[str, BlockBlastShape]:
    library = defaultdict()
    for base in bases:
        current = base  # Shape is a frozen dataclass so can't manipulate directly
        seen_coords = []
        rotation = 0
        for _ in range(4):
            if current.coordinates not in seen_coords:
                seen_coords.append(current.coordinates)
                library[f"{current.name}_{rotation}"] = current
                rotation += 1
            current = current.rotate()

    return library


SHAPES = generate_library(BASE_SHAPES)
ROW_GRID_SIZE = 8
COL_GRID_SIZE = 8
