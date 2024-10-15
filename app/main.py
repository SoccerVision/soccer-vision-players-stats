from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="Soccer Simulator API",
    description="An API to generate soccer teams and players.",
    version="1.0.0",
)

# Define the allowed origins
origins = [
    "https://soccersimulator.github.io",  # Your GitHub Pages URL
    "http://localhost:3000",
]

# Add CORS middleware to the FastAPI app (not to the router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the router for your API
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)