from dataclasses import dataclass, field


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

    def __getitem__(self, pos: tuple[int, int]) -> int | str:
        # This looks weird, but we want to check if coords are inside the board limits
        if pos not in self:
            return "OUT_OF_BOUND"
        row, col = pos
        return self.grid[row][col]

    def __setitem__(self, pos: tuple[int, int], value: int | str) -> None:
        if pos in self:
            row, col = pos
            self.grid[row][col] = value
