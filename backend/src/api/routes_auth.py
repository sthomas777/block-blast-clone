from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.database import get_session
from backend.src.repositories.player_repo import PlayerRepository
from backend.src.schemas.auth import AuthResponse, PlayerResponse, RegisterRequest
from backend.src.services.auth_service import (
    create_access_token,
    hash_password,
    oauth2_scheme,
    settings,
    verify_access_token,
    verify_password,
)

router = APIRouter(prefix="/api/auth")


def get_repo(session: AsyncSession = Depends(get_session)) -> PlayerRepository:
    return PlayerRepository(session)


@router.post("/register", response_model=PlayerResponse)
async def register(
    request: RegisterRequest,
    repo: PlayerRepository = Depends(get_repo),
) -> PlayerResponse:
    if await repo.get_by_username(request.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    player = await repo.create(
        request.username,
        hash_password(request.password.get_secret_value()),
    )
    return PlayerResponse(player_id=player.player_id, username=player.username)


@router.post("/token", response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: PlayerRepository = Depends(get_repo),
) -> AuthResponse:
    player = await repo.get_by_username(form_data.username)
    if not player or not verify_password(form_data.password, player.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password or Username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        data={"sub": str(player.player_id)},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return AuthResponse(access_token=token)


@router.get("/me", response_model=PlayerResponse)
async def get_current_player(
    token: str = Depends(oauth2_scheme),
    repo: PlayerRepository = Depends(get_repo),
) -> PlayerResponse:
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
    return PlayerResponse(player_id=player.player_id, username=player.username)
