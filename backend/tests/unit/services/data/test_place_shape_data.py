from backend.src.game.session import GameState
from backend.src.schemas.game import PlaceShapeResponse


# Expected response structure (shape name will be determined at test time)
def get_expected_place_shape_response(shape_name: str):
    return PlaceShapeResponse(
        game_id="1111-2222-3333-4444",
        score=0,
        shape=shape_name,
        status=GameState.PLAYER_TURN,
        placement=(3, 3),
    )
