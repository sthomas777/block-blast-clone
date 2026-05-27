from dataclasses import dataclass, replace


@dataclass(frozen=True)
class BlockBlastShape:
    name: str
    coordinates: list[tuple[int, int]]
    color: str

    def rotate(self):
        rotated = [(col, -row) for row, col in self.coordinates]

        # Want to normalize since before refactor we started each block at (0,x)
        min_row = min(row for row, col in rotated)
        min_col = min(col for row, col in rotated)

        normalised = sorted(
            # pyrefly: ignore [unnecessary-type-conversion]
            [(int(row - min_row), int(col - min_col)) for row, col in rotated],
        )

        return replace(self, coordinates=normalised)
