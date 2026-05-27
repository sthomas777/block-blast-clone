from fastapi import FastAPI
from backend.src.api.routes_game import router as game_router

app = FastAPI(title="Block Blast API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Block Blast API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(game_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
