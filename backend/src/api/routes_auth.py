from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import get_authenticated_player, get_repo
from src.models.player import Player
from src.repositories.player_repo import PlayerRepository
from src.schemas.auth import AuthResponse, PlayerResponse, RegisterRequest
from src.services.auth_service import (
    create_access_token,
    hash_password,
    settings,
    verify_password,
)

router = APIRouter(prefix="/api/auth")


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
    player: Player = Depends(get_authenticated_player),
) -> PlayerResponse:
    return PlayerResponse(player_id=player.player_id, username=player.username)
