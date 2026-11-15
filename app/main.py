from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.auth import require_api_key
from app.api.rate_limit import rate_limit
from app.api.v2 import router as v2_router
from app.core.errors import GeneratorError
from app.version import OPTIONS_TAG, PLAYERS_TAG, TEAMS_TAG, VERSION

DESCRIPTION = """
Generates soccer squads and players with position-specific, age-aware stats.

**Start here:** `GET /api/v2/options` lists every level, age profile, template, formation, position and role.

- **Teams:** `GET /api/v2/team` for quick options, `POST /api/v2/team` for custom position counts and level mixes.
- **Players:** `GET /api/v2/player` for one player, `POST /api/v2/players` for a batch.
- **Reproducible:** every response returns a `seed`. Send it back with the same options to get the identical result.
"""

app = FastAPI(
    title="Soccer Vision API",
    description=DESCRIPTION,
    version=VERSION,
    openapi_tags=[
        {"name": OPTIONS_TAG, "description": "Every value the generator accepts"},
        {"name": TEAMS_TAG, "description": "Generate full squads"},
        {"name": PLAYERS_TAG, "description": "Generate individual players"},
    ],
)

# No CORS middleware: this API is server-to-server only (no browser caller exists - confirmed
# the old GitHub Pages frontend origin 404s and nothing in soccer-vision calls this client-side),
# so a browser's same-origin policy already blocks it. The real access boundary is require_api_key
# below, not CORS - don't "fix" this by adding permissive CORS headers.


@app.exception_handler(GeneratorError)
async def generator_error_handler(request: Request, exc: GeneratorError):
    # Invalid option combinations (e.g. role not valid for the position) are client errors,
    # always written to be safe to echo back. A plain ValueError (a bug, not a deliberate
    # rejection) is not caught here and 500s instead.
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


app.include_router(
    v2_router,
    prefix="/api",
    dependencies=[Depends(require_api_key), Depends(rate_limit)],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
