"""Real-football reference data used by the player model.

Sources of the numbers are public averages for top-flight European football:
- Heights: goalkeepers ~189 cm, centre-backs ~187 cm, wingers ~175 cm.
- Footedness: ~22% of players are left-footed; wide players usually play on the side of
  their strong foot, except "inverted" wingers who cut inside onto it.
- Age: pace peaks around 24-27, strength around 26-30, technique stays flat until ~31,
  game intelligence (decisions, positioning, composure) keeps improving into the early 30s,
  goalkeepers peak around 29-33.
Base stat configs (app/core/levels/...) describe a player in his prime; the factors below scale
those by age.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

POSITIONS: Tuple[str, ...] = ("goalkeeper", "defender", "fullback", "midfielder", "winger", "striker")
LEVELS: Tuple[str, ...] = ("weaker", "normal", "excellent")
SIDES: Tuple[str, ...] = ("L", "C", "R")


@dataclass(frozen=True)
class PositionSpec:
    height: Tuple[float, float, int, int]  # mean, std_dev, min, max (cm)
    sides: Tuple[str, ...]                  # sides this position can play
    left_foot: Dict[str, float]             # P(left-footed) for each side the position can play
    roles: Tuple[str, ...]
    defensive: bool                         # small players get no dribbling bonus


POSITION_SPECS: Dict[str, PositionSpec] = {
    "goalkeeper": PositionSpec((189, 4, 178, 201), ("C",), {"C": 0.20}, ("shot_stopper", "sweeper_keeper"), True),
    "defender": PositionSpec((187, 4, 176, 200), ("L", "C", "R"), {"L": 0.40, "C": 0.15, "R": 0.05}, ("stopper", "ball_playing"), True),
    "fullback": PositionSpec((179, 5, 166, 192), ("L", "R"), {"L": 0.80, "R": 0.05}, ("defensive", "wing_back"), True),
    "midfielder": PositionSpec((179, 6, 163, 195), ("C",), {"C": 0.20},
                               ("defensive_mid", "box_to_box", "playmaker", "attacking_mid"), False),
    "winger": PositionSpec((175, 5, 162, 188), ("L", "R"), {"L": 0.35, "R": 0.35},  # many wingers are inverted
                           ("traditional", "inside_forward"), False),
    "striker": PositionSpec((182, 6, 165, 198), ("C",), {"C": 0.20},
                            ("poacher", "target_man", "complete_forward", "false_nine"), False),
}

# Weak foot on the common 1-5 star scale (5 = fully two-footed, very rare).
WEAK_FOOT_STARS_WEIGHTS: Dict[int, float] = {1: 0.05, 2: 0.45, 3: 0.38, 4: 0.10, 5: 0.02}


def legacy_weak_foot_level(stars: int) -> int:
    """Map 1-5 stars to the old 1-3 `weak_foot_level` field (kept for v1 clients)."""
    return 1 if stars <= 2 else (2 if stars == 3 else 3)


# Additive role modifiers. Key "category" applies to every stat in it, "category.stat" to one stat.
ROLE_MODIFIERS: Dict[str, Dict[str, Dict[str, int]]] = {
    "goalkeeper": {
        "shot_stopper": {"goalkeeping.reflexes": 4, "goalkeeping.one_on_one": 3, "goalkeeping.kicking": -5},
        "sweeper_keeper": {"goalkeeping.kicking": 8, "goalkeeping.one_on_one": 3,
                           "athletic.speed": 5, "athletic.acceleration": 5, "goalkeeping.aerial_ability": -3},
    },
    "defender": {
        "stopper": {"defense.tackling": 4, "athletic.physical_power": 5, "athletic.heading": 4,
                    "playmaking.passing": -5},
        "ball_playing": {"playmaking.passing": 10, "playmaking.creative": 5, "mental.composure": 5,
                         "defense.tackling": -3},
    },
    "fullback": {
        "defensive": {"defense": 5, "attack.off_the_ball": -6, "playmaking.crossing": -5},
        "wing_back": {"playmaking.crossing": 6, "attack.off_the_ball": 8, "athletic.speed": 3,
                      "defense.marking": -5, "defense.positioning": -5},
    },
    "midfielder": {
        "defensive_mid": {"defense": 12, "attack": -8, "athletic.physical_power": 5},
        "box_to_box": {"defense": 5, "attack": 5, "mental.teamwork": 5},
        "playmaker": {"playmaking.passing": 6, "playmaking.creative": 8, "mental.decisions": 5, "defense": -5},
        "attacking_mid": {"attack": 12, "playmaking.creative": 6, "defense": -10},
    },
    "winger": {
        "traditional": {"playmaking.crossing": 8, "athletic.speed": 3, "attack.finishing": -5},
        "inside_forward": {"attack.finishing": 8, "attack.long_shots": 5, "playmaking.crossing": -6},
    },
    "striker": {
        "poacher": {"attack.finishing": 5, "attack.off_the_ball": 6, "athletic.physical_power": -6,
                    "playmaking.passing": -5},
        "target_man": {"athletic.heading": 10, "athletic.jumping": 8, "athletic.physical_power": 12,
                       "athletic.speed": -6, "athletic.acceleration": -6},
        "complete_forward": {"playmaking.passing": 6, "playmaking.creative": 5, "athletic.dribbling": 4},
        "false_nine": {"playmaking.creative": 10, "playmaking.passing": 8, "attack.finishing": -4,
                       "athletic.physical_power": -5},
    },
}

# Age curves: (age, factor) points, linearly interpolated, flat outside the range.
AGE_CURVES: Dict[str, List[Tuple[int, float]]] = {
    "pace": [(16, .86), (19, .94), (22, .99), (24, 1.0), (27, 1.0), (30, .95), (33, .88), (36, .80)],
    "strength": [(16, .78), (19, .90), (23, .98), (26, 1.0), (30, 1.0), (33, .95), (36, .90)],
    "technical": [(16, .80), (19, .90), (23, .97), (26, 1.0), (31, 1.0), (34, .96), (37, .92)],
    "intelligence": [(16, .75), (19, .85), (23, .93), (27, .98), (29, 1.0), (33, 1.02), (36, 1.0)],
    "goalkeeping": [(16, .75), (19, .85), (23, .93), (27, .98), (29, 1.0), (34, 1.0), (37, .95), (40, .88)],
    "personality": [(16, 1.0), (40, 1.0)],
}

STAT_AGE_GROUP: Dict[str, str] = {
    "speed": "pace", "acceleration": "pace",
    "physical_power": "strength", "jumping": "strength", "heading": "strength",
    "ball_control": "technical", "dribbling": "technical", "passing": "technical", "crossing": "technical",
    "creative": "technical", "finishing": "technical", "long_shots": "technical", "tackling": "technical",
    "free_kicks": "technical", "penalty": "technical",
    "composure": "intelligence", "decisions": "intelligence", "positioning": "intelligence",
    "marking": "intelligence", "off_the_ball": "intelligence",
    "aggression": "personality", "teamwork": "personality",
}


def _interpolate(points: Sequence[Tuple[int, float]], age: float) -> float:
    if age <= points[0][0]:
        return points[0][1]
    for (a0, f0), (a1, f1) in zip(points, points[1:]):
        if age <= a1:
            return f0 + (f1 - f0) * (age - a0) / (a1 - a0)
    return points[-1][1]


def age_factor(category: str, stat: str, age: int) -> float:
    group = "goalkeeping" if category == "goalkeeping" else STAT_AGE_GROUP.get(stat, "technical")
    return _interpolate(AGE_CURVES[group], age)


# Position-weighted overall rating (weights are normalised over the stats a player has).
OVERALL_WEIGHTS: Dict[str, Dict[str, float]] = {
    "goalkeeper": {"goalkeeping.reflexes": 25, "goalkeeping.handling": 20, "goalkeeping.one_on_one": 20,
                   "goalkeeping.aerial_ability": 15, "goalkeeping.kicking": 10,
                   "mental.composure": 5, "mental.decisions": 5},
    "defender": {"defense.tackling": 20, "defense.marking": 20, "defense.positioning": 15,
                 "athletic.heading": 10, "athletic.physical_power": 10, "athletic.jumping": 5,
                 "athletic.speed": 5, "mental.composure": 5, "playmaking.passing": 5, "mental.decisions": 5},
    "fullback": {"defense.tackling": 15, "defense.marking": 12, "defense.positioning": 10,
                 "athletic.speed": 15, "athletic.acceleration": 10, "playmaking.crossing": 12,
                 "playmaking.passing": 8, "athletic.dribbling": 5, "attack.off_the_ball": 5, "mental.teamwork": 8},
    "midfielder": {"playmaking.passing": 20, "playmaking.creative": 15, "athletic.ball_control": 12,
                   "mental.decisions": 10, "mental.composure": 8, "attack.long_shots": 7,
                   "defense.positioning": 8, "defense.tackling": 8, "mental.teamwork": 7, "athletic.dribbling": 5},
    "winger": {"athletic.speed": 14, "athletic.acceleration": 14, "athletic.dribbling": 16,
               "playmaking.crossing": 14, "athletic.ball_control": 12, "attack.finishing": 10,
               "attack.off_the_ball": 10, "playmaking.passing": 5, "playmaking.creative": 5},
    "striker": {"attack.finishing": 25, "attack.off_the_ball": 18, "mental.composure": 10,
                "athletic.ball_control": 10, "athletic.heading": 8, "athletic.speed": 8,
                "athletic.acceleration": 8, "athletic.dribbling": 7, "athletic.physical_power": 6},
}

# Thresholds above which strikers/creators become better penalty and free-kick takers.
SET_PIECE_THRESHOLD: Dict[str, int] = {"weaker": 55, "normal": 70, "excellent": 90}

# Conventional shirt numbers, tried in order before a random free number.
PREFERRED_NUMBERS: Dict[Tuple[str, Optional[str]], List[int]] = {
    ("goalkeeper", None): [1, 13, 12, 23, 31],
    ("fullback", "L"): [3, 15, 26],
    ("fullback", "R"): [2, 22, 12],
    ("defender", None): [4, 5, 6, 15, 16, 24],
    ("midfielder", "defensive_mid"): [6, 16, 4, 14],
    ("midfielder", "box_to_box"): [8, 14, 16, 18],
    ("midfielder", "playmaker"): [10, 8, 14, 20],
    ("midfielder", "attacking_mid"): [10, 20, 14, 18],
    ("midfielder", None): [8, 6, 10, 14, 16, 18, 20],
    ("winger", "L"): [11, 17, 19],
    ("winger", "R"): [7, 17, 19],
    ("striker", None): [9, 10, 19, 20, 21],
}


def preferred_numbers(position: str, side: Optional[str], role: Optional[str] = None) -> List[int]:
    return (PREFERRED_NUMBERS.get((position, role)) or PREFERRED_NUMBERS.get((position, side))
            or PREFERRED_NUMBERS.get((position, None), []))
