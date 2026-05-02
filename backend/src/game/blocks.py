BLOCKS: dict[str, list[tuple[int, int]]] = {
    "single_cell": [(0,0)],
    "square": [(0,0), (0,1), (1,0), (1,1)],
    "horizontal_line": [(0,0), (0,1), (0,2)],
    "vertical_line": [(0,0), (1,0), (2,0)],
    "l_shape": [(0,0), (1,0), (2,0), (2,1)],
    "t_shape": [(0,0), (1,0), (2,0), (1,1)],
}
