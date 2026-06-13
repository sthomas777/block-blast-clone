from dataclasses import dataclass
from src.game.board import GameBoard
from src.game.shapes import ShapeManager
from src.game.scoring import ScoringEngine
from src.models.shape import BlockBlastShape


@dataclass
class GameEngine:
    board: GameBoard
    shape_manager: ShapeManager
    scoring: ScoringEngine

    def can_place_shape(
        self,
        shape: BlockBlastShape,
        position: tuple[int, int],
    ) -> bool:
        return self.board.can_place_at(shape.coordinates, position)

    def place_shape(self, shape: BlockBlastShape, position: tuple[int, int]) -> None:
        if self.can_place_shape(shape, position):
            self.board.place_shape(shape.coordinates, position, shape.color)
            self.shape_manager.remove_shape(shape)

    def process_board(self) -> int:
        lines_cleared = self.board.clear_lines()
        self.scoring.add_lines_cleared(lines_cleared)

        if not self.shape_manager.has_shapes():
            self.shape_manager.generate_new_set()

        return lines_cleared

    def has_valid_moves(self) -> bool:
        for shape in self.shape_manager.get_current_shapes():
            for row in range(self.board.rows):
                for col in range(self.board.cols):
                    if self.can_place_shape(shape, (row, col)):
                        return True
        return False

    def get_score(self) -> int:
        return self.scoring.get_score()
