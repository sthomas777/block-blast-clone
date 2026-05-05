from dataclasses import dataclass, field
from random import choice
from backend.src.models.shape import BlockBlastShape


@dataclass
class ShapeManager:
    available_shapes: dict[str, BlockBlastShape]
    current_shapes: list[BlockBlastShape] = field(default_factory=list)

    def generate_new_set(self) -> list[BlockBlastShape]:
        self.current_shapes = [choice(list(self.available_shapes.values())) for _ in range(3)]
        return self.current_shapes

    def remove_shape(self, shape: BlockBlastShape) -> None:
        if shape in self.current_shapes:
            self.current_shapes.remove(shape)

    def get_current_shapes(self) -> list[BlockBlastShape]:
        return self.current_shapes

    def has_shapes(self) -> bool:
        return len(self.current_shapes) > 0
