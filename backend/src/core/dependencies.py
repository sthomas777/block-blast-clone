from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.models.player import Player
from src.repositories.player_repo import PlayerRepository
from src.repositories.score_repo import ScoreRepository
from src.services.auth_service import oauth2_scheme, verify_access_token
from src.services.game_service import GameService

game_service = GameService()


def get_game_service() -> GameService:
    return game_service


def get_repo(session: AsyncSession = Depends(get_session)) -> PlayerRepository:
    return PlayerRepository(session)


def get_score_repo(session: AsyncSession = Depends(get_session)) -> ScoreRepository:
    return ScoreRepository(session)


async def get_authenticated_player(
    token: str = Depends(oauth2_scheme),
    repo: PlayerRepository = Depends(get_repo),
) -> Player:
    player_id = verify_access_token(token)
    if not player_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        player_id_int = int(player_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    player = await repo.get_by_id(player_id_int)
    if not player:
        raise HTTPException(status_code=404, detail="User not found")
    return player
