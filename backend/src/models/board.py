from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class BlockBlastBoard:
    rows: int
    cols: int
    grid: list[list[int | str]] = field(init=False)

    def __post_init__(self) -> None:
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def __contains__(self, pos: tuple[int, int]) -> bool:
        row, col = pos
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __getitem__(self, key: tuple[int, int] | int) -> int | str | list:
        if isinstance(key, int):
            if key < 0 or key >= self.rows:
                raise IndexError("Index out of range. Board has %s rows", self.rows)
            return self.grid[key]

        # Existing coordinate logic
        if key not in self:
            raise IndexError(
                "Index out of range. Board is %s by %s", self.rows, self.cols
            )
        row, col = key
        return self.grid[row][col]

    def __setitem__(self, key: tuple[int, int] | int, value: int | str | list) -> None:
        if isinstance(key, int):
            if 0 <= key < self.rows:
                self.grid[key] = value
            return

        if isinstance(key, tuple):
            if key in self:
                row, col = key
                self.grid[row][col] = value

    def __iter__(self) -> Iterator[list[int | str]]:
        return iter(self.grid)
