import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes_auth import router as auth_router
from src.api.routes_score import router as score_router
from src.api.ws_game import router as ws_game_router
from src.core.lifespan import lifespan
from src.services.game_service import InvalidGameID, InvalidPosition


app = FastAPI(title="Block Blast API", version="0.1.0", lifespan=lifespan)


@app.exception_handler(InvalidPosition)
def invalid_position_handler(request, exc) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(InvalidGameID)
def invalid_game_id_handler(request, exc) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Block Blast API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


cors_origins = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ws_game_router)
app.include_router(auth_router)
app.include_router(score_router)
