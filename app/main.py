# app/main.py

from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="Soccer Simulator API",
    description="An API to generate soccer teams and players.",
    version="1.0.0",
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)