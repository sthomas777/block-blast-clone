from backend.src.game.session import GameState
from backend.src.models.shape import BlockBlastShape
from backend.src.schemas.game import GameStateResponse


# Expected response structure (shape name will be determined at test time)
expected_placement_response = GameStateResponse(
    game_id="1111-2222-3333-4444",
    grid=[
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, "#f0a000", 0, 0],
        [0, 0, 0, "#f0a000", "#f0a000", "#f0a000", 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    score=0,
    shape=[
        BlockBlastShape(
            name="J",
            coordinates=[(0, 0), (0, 1), (1, 0), (2, 0)],
            color="#0000f0",
        ),
        BlockBlastShape(
            name="S",
            coordinates=[(0, 1), (0, 2), (1, 0), (1, 1)],
            color="#00f000",
        ),
    ],
    status=GameState.PLAYER_TURN,
    game_over=False,
)
