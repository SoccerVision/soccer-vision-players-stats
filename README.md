# Soccer Vision API

FastAPI service that generates soccer squads and players with position-specific, age-aware stats.

- **Live:** https://soccer-api.dev-spirit.com (Swagger UI at [`/docs`](https://soccer-api.dev-spirit.com/docs))
- **Frontend:** https://soccervision.github.io

## Run locally

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync                                   # creates .venv with app + dev dependencies
uv run uvicorn app.main:app --reload      # http://127.0.0.1:8000/docs
uv run pytest                             # 106 tests
```

## API

Every response from v2 includes a `seed`. Send the same seed and options again to get the identical result.

| Method | Path | What it does |
|---|---|---|
| GET | `/api/v2/options` | Lists every level, age profile, template, formation, position and role |
| GET | `/api/v2/team` | Squad from query options: `level`, `age_profile`, `min_age`, `max_age`, `template`, `formation`, `nationality`, `seed` |
| POST | `/api/v2/team` | Same, plus custom position counts and `level_weights` for mixed squads |
| GET | `/api/v2/team/{seed}/player/{index}` | One player from a seeded squad |
| GET | `/api/v2/player` | One player: `position`, `level`, `age`, `side`, `role`, `dominant_foot`, `seed` |
| POST | `/api/v2/players` | Up to 60 players with the same filters |

**Options at a glance**

- Levels: `weaker`, `normal`, `excellent`, `mixed` (default odds 2% excellent / 10% weaker / 88% normal).
- Templates: `uefa25` (25-man squad), `formation` (XI + backup XI + 3rd GK), `youth`, `legacy`, `legacy_core`.
- Formations: `4-4-2`, `4-3-3`, `4-2-3-1`, `3-5-2`, `3-4-3`, `5-3-2`.
- Age profiles: `realistic` (17-36, most around 26), `youth`, `young`, `prime`, `veteran`, `legacy`.

### v1 (unchanged, used by the frontend)

`GET /api/team`, `/api/team/weaker`, `/api/team/normal`, `/api/team/excellent`, `/api/team/younger`,
`/api/team/player/{index}`. They now also include the v2 fields (`overall`, `role`, `side`, ...).

## How players are generated

1. Base stats come from the level + position config in `app/core/levels/`.
2. Role modifiers (e.g. target man: +heading/strength, -pace) from `app/core/realism.py`.
3. Age curves per attribute: pace peaks 24-27, strength 26-30, technique flat to ~31,
   decisions/composure/positioning improve into the early 30s, goalkeepers peak ~29-33.
4. Fitness changes athletic stats only; height is compared with the position's average height.
5. `overall` is a position-weighted rating; `potential` is given to players aged 23 or less.

## Deploy

Hosted on Vercel (project `soccer-vision-api`); the entrypoint is set in `pyproject.toml`
(`[tool.vercel] entrypoint = "app.main:app"`).

```bash
vercel deploy          # preview
vercel deploy --prod   # production (soccer-api.dev-spirit.com)
```

## Positions (English / Hebrew)

```txt
goalkeeper - שוער
defender   - בלם
fullback   - מגן
midfielder - קשר
striker    - חלוץ
winger     - וינגר
```
