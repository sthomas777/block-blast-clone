import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from backend.src.core.dependencies import get_game_service
from backend.src.schemas.game import ErrorResponse
from backend.src.services.game_service import GameError
from backend.src.services.ws_handler import dispatch

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/game")
async def game_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    game_service = get_game_service()
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
    except WebSocketDisconnect:
        pass
