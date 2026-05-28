from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.src.api.routes_game import router as game_router
from backend.src.services.game_service import InvalidPosition, InvalidGameID

app = FastAPI(title="Block Blast API", version="0.1.0")


@app.exception_handler(InvalidPosition)
def invalid_position_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(InvalidGameID)
def invalid_game_id_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/")
def root():
    return {"message": "Block Blast API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(game_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
