GRID_SIZE = 8

def create_grid() -> list[list[int]]:
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def print_grid(grid: list[list[int]]) -> None:
    for row in grid:
        print(*row)

blocks: dict[str, list[tuple[int, int]]] = {
    "single_cell": [(0,0)],
    "square": [(0,0), (0,1), (1,0), (1,1)],
    "horizontal_line": [(0,0), (0,1), (0,2)],
    "vertical_line": [(0,0), (1,0), (2,0)],
    "l_shape": [(0,0), (1,0), (2,0), (2,1)],
    "t_shape": [(0,0), (1,0), (2,0), (1,1)],
}

def can_place_block(grid: list[list[int]], shape: str, row: int, col: int) -> bool:
    if grid[row][col] != 0:
        return False

    for block in blocks[shape]:
        if block[0] + row < 0 or block[0] + row >= GRID_SIZE:
            return False
        if block[1] + col < 0 or block[1] + col >= GRID_SIZE:
            return False
        if grid[block[0] + row][block[1] + col] != 0:
            return False
    return True

def place_block(grid: list[list[int]], shape: str, row: int, col: int) -> None:
    if can_place_block(grid, shape, row, col):
        for block in blocks[shape]:
            grid[block[0] + row][block[1] + col] = 1 # May come into issues with this later since I am using a reference of the list

def clear_lines(grid: list[list[int]]) -> int:
    row_lines_cleared = []
    col_lines_cleared = []
    for i, row in enumerate(grid):
        if all(row):
            row_lines_cleared.append(i)

    transpose_grid = list(map(list, zip(*grid)))
    for j, col in enumerate(transpose_grid):
        if all(col):
            col_lines_cleared.append(j)

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if i in row_lines_cleared or j in col_lines_cleared:
                grid[i][j] = 0 # May come into issues with this later since I am using a reference of the list

    return len(row_lines_cleared) + len(col_lines_cleared)

def calculate_score(lines_cleared: int) -> int:
    return sum(s * 10 for s in range(1, lines_cleared + 1))

gird = create_grid()
print_grid(gird)
print()
place_block(gird, "square", 6, 0)
place_block(gird, "square", 6, 2)
place_block(gird, "square", 6, 4)
place_block(gird, "square", 6, 6)
place_block(gird, "square", 4, 0)
place_block(gird, "square", 4, 4)
place_block(gird, "square", 4, 2)
place_block(gird, "square", 4, 4)
place_block(gird, "square", 2, 2)
place_block(gird, "horizontal_line", 0, 0)
place_block(gird, "vertical_line", 1, 0)
print_grid(gird)
print()
lines_cleared = clear_lines(gird)
print_grid(gird)
print(f"Lines Cleared:{lines_cleared}")
print(f"Score:{calculate_score(lines_cleared)}")