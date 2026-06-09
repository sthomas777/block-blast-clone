from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.src.api.routes_auth import router as auth_router
from backend.src.api.ws_game import router as ws_game_router
from backend.src.core.lifespan import lifespan
from backend.src.services.game_service import InvalidGameID, InvalidPosition


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ws_game_router)
app.include_router(auth_router)
