from backend.src.models.board import BlockBlastBoard
from backend.src.models.shape import BlockBlastShape


class BlockBlastLogic:
    @staticmethod
    def can_place_shape(
        board: BlockBlastBoard, shape: BlockBlastShape, offset: tuple[int, int]
    ) -> bool:
        row_offset, col_offset = offset
        for shape_row, shape_col in shape.coordinates:
            target_pos = (row_offset + shape_row, col_offset + shape_col)

            if target_pos not in board:
                return False

            # Checking is the cell is 0
            if board[target_pos]:
                return False
        return True

    @staticmethod
    def place_shape(
        board: BlockBlastBoard, shape: BlockBlastShape, offset: tuple[int, int]
    ) -> None:
        row_offset, col_offset = offset
        for shape_row, shape_col in shape.coordinates:
            board[shape_row + row_offset, shape_col + col_offset] = shape.color

    @staticmethod
    def clear_lines(board: BlockBlastBoard) -> int:
        # 1. Find indices of full rows
        # all(row) works because 0 is Falsy and strings are Truthy!
        row_indices = [i for i, row in enumerate(board.grid) if all(row)]

        col_indices = [
            j
            for j in range(board.cols)
            if all(board.grid[r][j] for r in range(board.rows))
        ]

        for r in row_indices:
            board.grid[r] = [0] * board.cols

        for c in col_indices:
            for r in range(board.rows):
                board.grid[r][c] = 0

        # Return total lines cleared (for scoring)
        return len(row_indices) + len(col_indices)
