from .blocks import BLOCKS

GRID_SIZE = 8


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def can_place(self, shape: str, row: int, col: int) -> bool:
        grid_copy = self.get_grid()
        for block in BLOCKS[shape]:
            if block[0] + row < 0 or block[0] + row >= GRID_SIZE:
                return False
            if block[1] + col < 0 or block[1] + col >= GRID_SIZE:
                return False
            if grid_copy[block[0] + row][block[1] + col] != 0:
                return False
        return True

    def place_shape(self, shape: str, row: int, col: int) -> None:
        if self.can_place(shape, row, col):
            for block in BLOCKS[shape]:
                self.grid[block[0] + row][block[1] + col] = (
                    1  # May come into issues with this later since I am using a reference of the list
                )

    def clear_lines(self) -> int:
        row_lines_cleared = []
        col_lines_cleared = []
        for i, row in enumerate(self.get_grid()):
            if all(row):
                row_lines_cleared.append(i)

        # Need to do this to see if the column is complete
        # Probably a better way of doing this
        transpose_grid = list(map(list, zip(*self.get_grid())))
        for j, col in enumerate(transpose_grid):
            if all(col):
                col_lines_cleared.append(j)

        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if i in row_lines_cleared or j in col_lines_cleared:
                    self.grid[i][j] = (
                        0  # May come into issues with this later since I am using a reference of the list
                    )

        return len(row_lines_cleared) + len(col_lines_cleared)

    def print_grid(self) -> None:
        for row in self.get_grid():
            print(*row)

    def get_grid(self) -> list[list[int]]:
        return [row[:] for row in self.grid]
