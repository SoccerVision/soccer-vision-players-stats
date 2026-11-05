from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.endpoints import router as v1_router
from app.api.v2 import router as v2_router
from app.version import OPTIONS_TAG, PLAYERS_TAG, TEAMS_TAG, V1_TAG, VERSION

DESCRIPTION = f"""
Generates soccer squads and players with position-specific, age-aware stats.

**Code version {VERSION}.** The version badge and the tags below are this version, taken from `pyproject.toml`.

**Start here:** `GET /api/v2/options` lists every level, age profile, template, formation, position and role.

- **Teams:** `GET /api/v2/team` for quick options, `POST /api/v2/team` for custom position counts and level mixes.
- **Players:** `GET /api/v2/player` for one player, `POST /api/v2/players` for a batch.
- **Reproducible:** every response returns a `seed`. Send it back with the same options to get the identical result.
- **v1 routes** (`/api/team/...`) are unchanged for existing clients.
"""

app = FastAPI(
    title="Soccer Vision API",
    description=DESCRIPTION,
    version=VERSION,
    openapi_tags=[
        {"name": OPTIONS_TAG, "description": f"Every value the generator accepts. Code version {VERSION}."},
        {"name": TEAMS_TAG, "description": f"Generate full squads. Code version {VERSION}."},
        {"name": PLAYERS_TAG, "description": f"Generate individual players. Code version {VERSION}."},
        {"name": V1_TAG, "description": f"Original endpoints, kept for existing clients. Shipped in code version {VERSION}."},
    ],
)

origins = [
    "https://soccervision.github.io",  # Frontend on GitHub Pages
    "https://dev-spirit.com",
    "https://www.dev-spirit.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    # Invalid option combinations (e.g. role not valid for the position) are client errors
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


app.include_router(v1_router, prefix="/api")
app.include_router(v2_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
