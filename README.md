# Soccer Vision API

FastAPI service that generates soccer squads and players with position-specific, age-aware stats.

- **Live:** https://soccer-api.dev-spirit.com (Swagger UI at [`/docs`](https://soccer-api.dev-spirit.com/docs))
- **Frontend:** https://soccervision.github.io

## Run locally

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync                                   # creates .venv with app + dev dependencies
uv run uvicorn app.main:app --reload      # http://127.0.0.1:8000/docs
uv run pytest                             # 105 tests
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
- Age profiles: `realistic` (16-40, the age spread of real first-team squads: 18% aged 21 or under, 6% 34+), `youth`, `young`, `prime`, `veteran`, `legacy`.

## How players are generated

1. Base stats come from the level + position config in `app/core/levels/`. The excellent level is pulled towards
   FIFA 23's 78+ players (about 83 in a position's key skill): 90+ is rare, as it is for the very best real players.
   Decisions (intelligence) are a little better at a higher level but spread wide; aggression and teamwork are
   character, at random for every position and level.
2. Heading is a skill (accuracy) with its own level by position; jumping is athletic. Height changes neither.
3. Role modifiers (e.g. target man: +heading/strength, -pace) from `app/core/realism.py`.
4. Age curves per attribute: pace peaks about 23-27 and falls from about 29; strength grows to about 29; technique is
   flat to ~31; decisions/composure/positioning improve into the early 30s; goalkeepers peak ~29-33. Stamina grows
   from about three quarters of its peak at 17.
5. Fitness changes athletic stats only. Height, against the position's average: a taller player is stronger and
   slower to get going.
6. Feet: the share of left-footers by slot (left back 85%, left centre-back 50%, left winger 20% - most play inverted);
   the weak foot in 1-5 stars, better players more two-footed. The weak foot gives no bonus to other skills.
7. `overall` is a position-weighted rating; `potential` is given to players aged 23 or less.

Every number in `app/core/realism.py` names its source: REAL (measured: CIES, StatsBomb, FIFA 23 ages, heights and
feet), GAME (EA's FIFA 23 ratings) or DESIGN (our choice).

## Deploy

Hosted on Vercel (project `soccer-vision-api`); the entrypoint is set in `pyproject.toml`
(`[tool.vercel] entrypoint = "app.main:app"`).

```bash
vercel deploy          # preview
vercel deploy --prod   # production (soccer-api.dev-spirit.com)
```

A push to `main` bumps the patch version in `pyproject.toml`. That version is the badge at the top of `/docs`.

## Positions (English / Hebrew)

```txt
goalkeeper - שוער
defender   - בלם
fullback   - מגן
midfielder - קשר
striker    - חלוץ
winger     - וינגר
```
