import logging

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from src.core.dependencies import get_game_service, get_score_repo
from src.repositories.score_repo import ScoreRepository
from src.schemas.game import ErrorResponse
from src.services.auth_service import verify_access_token
from src.services.game_service import GameError, GameService
from src.services.ws_handler import dispatch

logger = logging.getLogger(__name__)

router = APIRouter()


def _resolve_player_id(token: str | None) -> int | None:
    if not token:
        return None
    sub = verify_access_token(token)
    if not sub:
        return None
    try:
        return int(sub)
    except (TypeError, ValueError):
        return None


@router.websocket("/ws/game")
async def game_websocket(
    websocket: WebSocket,
    token: str | None = Query(default=None),
    game_service: GameService = Depends(get_game_service),
    score_repo: ScoreRepository = Depends(get_score_repo),
) -> None:
    await websocket.accept()
    player_id = _resolve_player_id(token)
    game_id: str | None = None

    try:
        while True:
            raw = await websocket.receive_json()

            # Tiered error handling: validation and domain errors are
            # recoverable (report and keep the socket open); anything else is
            # a bug — log it and return a generic message so we don't leak
            # internals to the client.
            try:
                response = dispatch(raw, game_id, game_service)
            except ValidationError as exc:
                await websocket.send_json(
                    jsonable_encoder(
                        ErrorResponse(code="validation_error", message=str(exc)),
                    ),
                )
                continue
            except GameError as exc:
                await websocket.send_json(
                    jsonable_encoder(
                        ErrorResponse(code="game_error", message=str(exc)),
                    ),
                )
                continue
            except Exception:
                logger.exception("Unhandled error in ws dispatch (game_id=%s)", game_id)
                await websocket.send_json(
                    jsonable_encoder(
                        ErrorResponse(
                            code="internal_error",
                            message="Internal server error",
                        ),
                    ),
                )
                continue

            if response.game_id:
                game_id = response.game_id
            await websocket.send_json(jsonable_encoder(response))

            # Persist the final score and drop the in-memory game on game over.
            if response.game_over and game_id:
                await game_service.end_game(game_id, score_repo, player_id)
                game_id = None
    except WebSocketDisconnect:
        pass
