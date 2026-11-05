"""v2 API: every generation option is exposed and documented in Swagger (/docs)."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api import schemas as s
from app.core import realism
from app.core.generator import (AGE_PROFILES, REAL_AGES, FORMATIONS, TEMPLATES, GenerationOptions, Squad,
                                generate_players, generate_squad, squad_summary)
from app.version import OPTIONS_TAG as INFO_TAG, PLAYERS_TAG as PLAYER_TAG, TEAMS_TAG as TEAM_TAG

router = APIRouter(prefix="/v2")


def _val(enum_value):
    return enum_value.value if enum_value is not None else None


def _team_response(squad: Squad) -> dict:
    return {"seed": squad.seed, "summary": squad_summary(squad.players),
            "players": [p.to_dict() for p in squad.players]}


def _team_options(req: s.TeamRequest) -> GenerationOptions:
    return GenerationOptions(
        level=req.level.value,
        level_weights={k.value: v for k, v in req.level_weights.items()} if req.level_weights else None,
        age_profile=req.age_profile.value, min_age=req.min_age, max_age=req.max_age,
        template=req.template.value, formation=_val(req.formation),
        positions={k.value: v for k, v in req.positions.items()} if req.positions else None,
        nationalities=req.nationalities, seed=req.seed,
    )


def _team_query(level: s.Level = Query(s.Level("normal"), description="`mixed` uses the default odds (2% excellent, 10% weaker)"),
                age_profile: s.AgeProfile = Query(s.AgeProfile("realistic")),
                min_age: Optional[int] = Query(None, ge=15, le=45),
                max_age: Optional[int] = Query(None, ge=15, le=45),
                template: s.Template = Query(s.Template("uefa25"), description="Ignored when formation is set"),
                formation: Optional[s.Formation] = Query(None),
                nationality: Optional[List[str]] = Query(None, description="Repeat to give a pool"),
                seed: Optional[int] = Query(None, ge=0, description="Same seed + options = same squad")
                ) -> s.TeamRequest:
    return s.TeamRequest(level=level, age_profile=age_profile, min_age=min_age, max_age=max_age,
                         template=template, formation=formation, nationalities=nationality, seed=seed)


@router.get("/options", response_model=s.OptionsResponse, tags=[INFO_TAG],
            summary="List every value the generator accepts")
def get_options():
    return {
        "levels": [lvl.value for lvl in s.Level],
        "age_profiles": {name: (f"{lo}-{hi}" + (", the age spread of real first-team squads" if mode == REAL_AGES
                                                 else f", most around {mode}" if mode else ""))
                         for name, (lo, hi, mode) in AGE_PROFILES.items()},
        "templates": TEMPLATES,
        "formations": {name: [f"{slot.position}{'/' + slot.side if slot.side else ''}"
                              f"{' (' + slot.role + ')' if slot.role else ''}" for slot in xi]
                       for name, xi in FORMATIONS.items()},
        "positions": {name: {"sides": list(spec.sides), "roles": list(spec.roles),
                             "average_height_cm": spec.height[0]}
                      for name, spec in realism.POSITION_SPECS.items()},
    }


@router.get("/team", response_model=s.TeamResponse, tags=[TEAM_TAG], summary="Generate a squad (query options)")
def get_team(req: s.TeamRequest = Depends(_team_query)):
    return _team_response(generate_squad(_team_options(req)))


@router.post("/team", response_model=s.TeamResponse, tags=[TEAM_TAG],
             summary="Generate a squad (full control: custom counts, level weights)")
def post_team(req: s.TeamRequest):
    return _team_response(generate_squad(_team_options(req)))


@router.get("/team/{seed}/player/{index}", response_model=s.Player, tags=[TEAM_TAG],
            summary="One player from a seeded squad",
            description="Regenerates the squad for `seed` + the same query options and returns player `index` "
                        "(0-based).")
def get_team_player(seed: int, index: int,
                    level: s.Level = Query(s.Level("normal")),
                    age_profile: s.AgeProfile = Query(s.AgeProfile("realistic")),
                    min_age: Optional[int] = Query(None, ge=15, le=45),
                    max_age: Optional[int] = Query(None, ge=15, le=45),
                    template: s.Template = Query(s.Template("uefa25")),
                    formation: Optional[s.Formation] = Query(None),
                    nationality: Optional[List[str]] = Query(None)):
    if seed < 0:
        raise HTTPException(status_code=422, detail="seed must be >= 0")
    req = _team_query(level, age_profile, min_age, max_age, template, formation, nationality, seed)
    players = generate_squad(_team_options(req)).players
    if not 0 <= index < len(players):
        raise HTTPException(status_code=404, detail=f"index must be 0-{len(players) - 1}")
    return players[index].to_dict()


def _players(req: s.PlayersRequest) -> dict:
    options = GenerationOptions(
        level=req.level.value,
        level_weights={k.value: v for k, v in req.level_weights.items()} if req.level_weights else None,
        age_profile=req.age_profile.value, nationalities=req.nationalities, seed=req.seed)
    squad = generate_players(options, req.count, position=_val(req.position), side=_val(req.side),
                             role=_val(req.role), dominant_foot=_val(req.dominant_foot), age=req.age)
    return {"seed": squad.seed, "players": [p.to_dict() for p in squad.players]}


@router.get("/player", response_model=s.Player, tags=[PLAYER_TAG], summary="Generate one player")
def get_player(position: Optional[s.Position] = Query(None, description="Random when empty"),
               level: s.PlayerLevel = Query(s.PlayerLevel("normal")),
               age: Optional[int] = Query(None, ge=15, le=45),
               age_profile: s.AgeProfile = Query(s.AgeProfile("realistic")),
               side: Optional[s.Side] = Query(None),
               role: Optional[s.Role] = Query(None, description="Must belong to the position"),
               dominant_foot: Optional[s.Foot] = Query(None),
               nationality: Optional[List[str]] = Query(None),
               seed: Optional[int] = Query(None, ge=0)):
    req = s.PlayersRequest(count=1, level=s.Level(level.value), position=position, age=age, age_profile=age_profile,
                           side=side, role=role, dominant_foot=dominant_foot, nationalities=nationality, seed=seed)
    return _players(req)["players"][0]


@router.post("/players", response_model=s.PlayersResponse, tags=[PLAYER_TAG],
             summary="Generate several players with the same filters")
def post_players(req: s.PlayersRequest):
    return _players(req)
