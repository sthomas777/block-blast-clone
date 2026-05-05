from dataclasses import dataclass, field
from backend.src.models.board import BlockBlastBoard


@dataclass
class GameBoard:
    rows: int = 8
    cols: int = 8
    board: BlockBlastBoard = field(init=False)

    def __post_init__(self) -> None:
        self.board = BlockBlastBoard(rows=self.rows, cols=self.cols)

    @property
    def grid(self) -> list[list[int]]:
        return self.board.grid

    def can_place_at(self, shape_coords: list[tuple[int, int]], position: tuple[int, int]) -> bool:
        row_offset, col_offset = position
        for dr, dc in shape_coords:
            r, c = row_offset + dr, col_offset + dc
            if (r, c) not in self.board or self.board[r, c] != 0:
                return False
        return True

    def place_shape(self, shape_coords: list[tuple[int, int]], position: tuple[int, int]) -> None:
        row_offset, col_offset = position
        for dr, dc in shape_coords:
            self.board[row_offset + dr, col_offset + dc] = 1

    def clear_lines(self) -> int:
        row_indices = [i for i, row in enumerate(self.board) if all(row)]
        col_indices = [
            j for j in range(self.cols) if all(self.board[r, j] for r in range(self.rows))
        ]

        for r in row_indices:
            self.board[r] = [0] * self.cols

        for c in col_indices:
            for r in range(self.rows):
                self.board[r, c] = 0

        return len(row_indices) + len(col_indices)
