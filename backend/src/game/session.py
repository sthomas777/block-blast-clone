from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable

from backend.src.game.board import GameBoard
from backend.src.game.engine import GameEngine
from backend.src.game.shapes import ShapeManager
from backend.src.game.scoring import ScoringEngine
from backend.src.game.statemachine import StateMachine
from backend.src.models.shape import BlockBlastShape
from backend.src.game.constants import SHAPES


class GameState(Enum):
    START = auto()
    PLAYER_TURN = auto()
    SHAPE_PREVIEW = auto()
    LINES_CLEARED = auto()
    CHECKING_BOARD = auto()
    GAME_OVER = auto()


class GameEvent(Enum):
    START_GAME = auto()
    PREVIEW_SHAPE = auto()
    CONFIRM_PLACEMENT = auto()
    LINES_CLEARED = auto()


@dataclass
class GameContext:
    engine: GameEngine
    current_shape: BlockBlastShape | None = None
    current_position: tuple[int, int] = (0, 0)


game_state_machine: StateMachine[GameState, GameEvent, GameContext] = StateMachine()


@game_state_machine.transition(
    GameState.START,
    GameEvent.START_GAME,
    GameState.PLAYER_TURN,
)
def start_game(context: GameContext) -> None:
    context.engine.shape_manager.generate_new_set()


@game_state_machine.transition(
    GameState.SHAPE_PREVIEW,
    GameEvent.CONFIRM_PLACEMENT,
    GameState.LINES_CLEARED,
)
def place_current_shape(context: GameContext) -> None:
    if context.current_shape is None:
        return
    context.engine.place_shape(context.current_shape, context.current_position)


@game_state_machine.transition(
    GameState.LINES_CLEARED,
    GameEvent.LINES_CLEARED,
    GameState.CHECKING_BOARD,
)
def clear_lines_action(context: GameContext) -> None:
    context.engine.process_board()


@dataclass
class GameSession:
    board_size: tuple[int, int] = (6, 6)
    board: GameBoard = field(init=False)
    shape_manager: ShapeManager = field(init=False)
    scoring: ScoringEngine = field(init=False)
    engine: GameEngine = field(init=False)
    context: GameContext = field(init=False)
    state: GameState = field(default=GameState.START, init=False)
    listeners: dict[str, list[Callable]] = field(
        default_factory=lambda: {
            "shape_placed": [],
            "lines_cleared": [],
            "game_over": [],
        },
        init=False,
    )

    def __post_init__(self) -> None:
        self.board = GameBoard(rows=self.board_size[0], cols=self.board_size[1])
        self.shape_manager = ShapeManager(SHAPES)
        self.scoring = ScoringEngine()
        self.engine = GameEngine(self.board, self.shape_manager, self.scoring)
        self.context = GameContext(engine=self.engine)

    def on(self, event: str, callback: Callable) -> None:
        if event in self.listeners:
            self.listeners[event].append(callback)

    def emit(self, event: str, *args, **kwargs) -> None:
        for callback in self.listeners.get(event, []):
            callback(*args, **kwargs)

    def start(self) -> None:
        self.state = game_state_machine.handle(
            self.context,
            self.state,
            GameEvent.START_GAME,
        )

    def preview_shape(self, shape: BlockBlastShape, position: tuple[int, int]) -> bool:
        if not self.engine.can_place_shape(shape, position):
            return False

        self.context.current_shape = shape
        self.context.current_position = position
        self.state = GameState.SHAPE_PREVIEW
        return True

    def confirm_placement(self) -> None:
        self.state = game_state_machine.handle(
            self.context,
            self.state,
            GameEvent.CONFIRM_PLACEMENT,
        )
        self.emit(
            "shape_placed",
            self.context.current_shape,
            self.context.current_position,
        )

        self.state = game_state_machine.handle(
            self.context,
            self.state,
            GameEvent.LINES_CLEARED,
        )
        self.emit("lines_cleared", self.engine.get_score())

        if self.engine.has_valid_moves():
            self.state = GameState.PLAYER_TURN
        else:
            self.state = GameState.GAME_OVER
            self.emit("game_over", self.engine.get_score())

    def is_game_over(self) -> bool:
        return self.state == GameState.GAME_OVER

    def get_score(self) -> int:
        return self.engine.get_score()

    def get_available_shapes(self) -> list[BlockBlastShape]:
        return self.engine.shape_manager.get_current_shapes()

    def get_board_grid(self) -> list[list[int | str]]:
        return self.board.grid
