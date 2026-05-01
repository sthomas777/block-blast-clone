GRID_SIZE = 8

def create_grid() -> list[list[int]]:
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def print_grid(grid: list[list[int]]) -> None:
    for row in grid:
        print(*row)
