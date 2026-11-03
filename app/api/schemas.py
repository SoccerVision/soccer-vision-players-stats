"""Typed request/response models for the v2 API (they drive the Swagger UI)."""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core import realism
from app.core.generator import AGE_PROFILES, FORMATIONS, TEMPLATES


def _enum(name: str, values) -> type:
    return Enum(name, {v.replace("-", "_").upper() if not v[0].isdigit() else f"F_{v.replace('-', '_')}": v
                       for v in values}, type=str)


Level = _enum("Level", [*realism.LEVELS, "mixed"])
PlayerLevel = _enum("PlayerLevel", realism.LEVELS)
Position = _enum("Position", realism.POSITIONS)
Side = _enum("Side", realism.SIDES)
Foot = _enum("Foot", ["Left", "Right"])
AgeProfile = _enum("AgeProfile", AGE_PROFILES)
Template = _enum("Template", TEMPLATES)
Formation = _enum("Formation", FORMATIONS)
Role = _enum("Role", sorted({r for spec in realism.POSITION_SPECS.values() for r in spec.roles}))


# ---------- player ----------
class Mental(BaseModel):
    aggression: int
    teamwork: int
    decisions: int
    composure: int


class Defense(BaseModel):
    tackling: int
    marking: int
    positioning: int


class Attack(BaseModel):
    finishing: int
    long_shots: int
    off_the_ball: int


class Playmaking(BaseModel):
    creative: int
    passing: int
    crossing: int


class Athletic(BaseModel):
    physical_power: int
    ball_control: int
    dribbling: int
    jumping: int
    acceleration: int
    speed: int
    heading: int


class SetPieces(BaseModel):
    free_kicks: int
    penalty: int


class Goalkeeping(BaseModel):
    aerial_ability: int
    handling: int
    kicking: int
    one_on_one: int
    reflexes: int


class Stats(BaseModel):
    """All values are 1-99. Goalkeepers have `goalkeeping` instead of attack/defense/playmaking."""
    mental: Mental
    athletic: Athletic
    set_pieces: SetPieces
    defense: Optional[Defense] = None
    attack: Optional[Attack] = None
    playmaking: Optional[Playmaking] = None
    goalkeeping: Optional[Goalkeeping] = None


class PreferredFoot(BaseModel):
    dominant_foot: str
    weak_foot_level: int = Field(description="Legacy 1-3 scale (kept for v1 clients)")
    weak_foot_stars: int = Field(description="1-5 stars, 5 = fully two-footed")


class Player(BaseModel):
    id: str
    name: str
    shirt_number: int
    position: str
    side: str = Field(description="L, C or R")
    role: str
    level: str
    age: int
    height: int = Field(description="cm")
    preferred_foot: PreferredFoot
    weak_foot_stars: int
    stamina: int
    fitness: str = Field(description="Low, Moderate or Peak")
    nationality: str
    overall: int = Field(description="Position-weighted rating 1-99")
    potential: Optional[int] = Field(None, description="Expected peak overall; only for players aged 23 or less")
    squad_role: Optional[str] = Field(None, description="starter / bench when a formation is used")
    stats: Stats
    averages: Dict[str, int] = Field(description="Average per stat category")


# ---------- requests ----------
class TeamRequest(BaseModel):
    level: Level = Field(Level("normal"), description="`mixed` draws each player's level from `level_weights`")
    level_weights: Optional[Dict[PlayerLevel, float]] = Field(
        None, description="Only with level=mixed. Default: excellent 1, weaker 5, normal 44")
    age_profile: AgeProfile = AgeProfile("realistic")
    min_age: Optional[int] = Field(None, ge=15, le=45)
    max_age: Optional[int] = Field(None, ge=15, le=45)
    template: Template = Template("uefa25")
    formation: Optional[Formation] = Field(None, description="Builds starting XI + backup XI + 3rd GK (23)")
    positions: Optional[Dict[Position, int]] = Field(
        None, description="Custom squad, e.g. {\"goalkeeper\": 2, \"striker\": 4}. Overrides template/formation")
    nationalities: Optional[List[str]] = Field(None, min_length=1, max_length=50)
    seed: Optional[int] = Field(None, ge=0, description="Same seed + same options = same squad")

    model_config = ConfigDict(json_schema_extra={"examples": [
        {"level": "mixed", "level_weights": {"excellent": 3, "normal": 15, "weaker": 2},
         "age_profile": "realistic", "formation": "4-3-3", "seed": 42},
        {"level": "excellent", "positions": {"goalkeeper": 1, "defender": 4, "striker": 2}},
    ]})


class PlayersRequest(BaseModel):
    count: int = Field(5, ge=1, le=60)
    level: Level = Level("normal")
    level_weights: Optional[Dict[PlayerLevel, float]] = None
    position: Optional[Position] = Field(None, description="Random position when empty")
    side: Optional[Side] = None
    role: Optional[Role] = Field(None, description="Must belong to the position (see /api/v2/options)")
    dominant_foot: Optional[Foot] = None
    age: Optional[int] = Field(None, ge=15, le=45, description="Exact age; overrides age_profile")
    age_profile: AgeProfile = AgeProfile("realistic")
    nationalities: Optional[List[str]] = Field(None, min_length=1, max_length=50)
    seed: Optional[int] = Field(None, ge=0)


# ---------- responses ----------
class SquadSummary(BaseModel):
    count: int
    by_position: Dict[str, int]
    average_age: float
    average_overall: float
    starting_xi_overall: Optional[float] = None
    left_footed: int


class TeamResponse(BaseModel):
    seed: int = Field(description="Send this seed back to get the identical squad again")
    summary: SquadSummary
    players: List[Player]


class PlayersResponse(BaseModel):
    seed: int
    players: List[Player]


class PositionInfo(BaseModel):
    sides: List[str]
    roles: List[str]
    average_height_cm: float


class OptionsResponse(BaseModel):
    levels: List[str]
    age_profiles: Dict[str, str]
    templates: Dict[str, str]
    formations: Dict[str, List[str]]
    positions: Dict[str, PositionInfo]
