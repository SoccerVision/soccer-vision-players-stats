"""Real-football reference data used by the player model.

Every number says where it comes from. REAL = measured real-world data; GAME = EA's FIFA 23 ratings (designers'
opinions, the only source for some things); DESIGN = our choice, no source.
- Heights (REAL): CIES Football Observatory, Monthly Report 79 (Oct 2022): goalkeepers 190.0, centre-backs 187.4,
  full-backs 179.3, midfielders 177.8-180.4 cm; wingers and strikers from FIFA 23 (heights are real facts): 176.7 / 183.3.
- Footedness (REAL): StatsBomb, "Footedness: how important is it?" (M. Carter, 2024): left back 78%, left centre-back 56%,
  left winger 16% left-footed; the other slots from FIFA 23 starters in the top divisions (preferred foot is a real fact).
- Age spread (REAL): FIFA 23 first-team players of the top divisions (11,500; ages are real facts) - AGE_HISTOGRAM.
- Age curves (MIXED): peer-reviewed studies put the sprint peak at about 25.7 and a decline from about 28; the shape by age
  of pace, strength and stamina is FIFA 23's (survivorship bias at 32+: the real decline is at least as steep).
- Weak foot, heading accuracy, aggression (GAME): FIFA 23 top-division players by level band and position.
Base stat configs (app/core/levels/...) describe a player in his prime; the factors below scale those by age.
The FIFA 23 figures were counted from Hugging Face jsulz/FIFA23, 'male_players (legacy).csv' (FIFA 23 rows, league_level 1).
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
    # height: CIES / FIFA 23 (see above); left_foot: StatsBomb for LB, LCB, LW, FIFA 23 starters for the rest
    "goalkeeper": PositionSpec((189, 4.7, 178, 201), ("C",), {"C": 0.13}, ("shot_stopper", "sweeper_keeper"), True),
    "defender": PositionSpec((187, 4.7, 176, 200), ("L", "C", "R"), {"L": 0.50, "C": 0.11, "R": 0.05}, ("stopper", "ball_playing"), True),
    "fullback": PositionSpec((179, 5, 166, 192), ("L", "R"), {"L": 0.85, "R": 0.02}, ("defensive", "wing_back"), True),
    "midfielder": PositionSpec((179, 6, 163, 195), ("C",), {"C": 0.18},  # (by role: see LEFT_FOOT_BY_ROLE)
                               ("defensive_mid", "box_to_box", "playmaker", "attacking_mid"), False),
    "winger": PositionSpec((177, 5.5, 162, 190), ("L", "R"), {"L": 0.20, "R": 0.38},  # most wingers play on the side of their weaker foot (inverted)
                           ("traditional", "inside_forward"), False),
    "striker": PositionSpec((183, 6, 165, 199), ("C",), {"C": 0.16},
                            ("poacher", "target_man", "complete_forward", "false_nine"), False),
}

# P(left-footed) for the midfield roles (FIFA 23 starters: CDM 13%, CM 17-21%, CAM 24%)
LEFT_FOOT_BY_ROLE: Dict[str, float] = {"defensive_mid": 0.13, "box_to_box": 0.18, "playmaker": 0.18, "attacking_mid": 0.24}

# The age spread of a first-team squad (FIFA 23, 11,500 first-team players of the top divisions: mean 26.0, 18% aged 21 or
# under, 24% 30+, 6% 34+), share by age.
AGE_HISTOGRAM: Dict[int, float] = {
    16: 0.0008, 17: 0.0063, 18: 0.0194, 19: 0.0387, 20: 0.0498, 21: 0.0656, 22: 0.0810, 23: 0.0709, 24: 0.0738,
    25: 0.0786, 26: 0.0771, 27: 0.0662, 28: 0.0649, 29: 0.0623, 30: 0.0629, 31: 0.0467, 32: 0.0417, 33: 0.0317,
    34: 0.0226, 35: 0.0154, 36: 0.0099, 37: 0.0063, 38: 0.0035, 39: 0.0022, 40: 0.0011,
}

# Heading accuracy is a skill, not a jump: by position and level (GAME: FIFA 23 averages, top divisions, overall <60 / 60-72 /
# 78+). Height decides how high a player reaches - the match engine works that out from the height itself.
HEADING_BY_LEVEL: Dict[str, Dict[str, int]] = {
    "goalkeeper": {"weaker": 13, "normal": 14, "excellent": 15},
    "defender": {"weaker": 54, "normal": 66, "excellent": 80},
    "fullback": {"weaker": 44, "normal": 54, "excellent": 68},
    "midfielder": {"weaker": 46, "normal": 53, "excellent": 62},
    "winger": {"weaker": 41, "normal": 48, "excellent": 56},
    "striker": {"weaker": 54, "normal": 64, "excellent": 77},
}

# Aggression is a trait of the position, not of the level (GAME: FIFA 23, players rated 60-72; the spread is kept wide).
AGGRESSION_BY_POSITION: Dict[str, int] = {"goalkeeper": 26, "defender": 67, "fullback": 62, "midfielder": 62,
                                          "winger": 49, "striker": 54}

# Stamina by age (MIXED: FIFA 23 outfield players' stamina against ages 27-29) - a 17-year-old has about three quarters of it.
STAMINA_BY_AGE: List[Tuple[int, float]] = [(17, .76), (18, .78), (19, .82), (20, .86), (21, .89), (22, .93), (23, .94), (24, .98),
                                           (27, 1.0), (30, .99), (32, .98), (33, .96), (34, .95), (35, .91), (36, .85)]

# Weak foot on the common 1-5 star scale (5 = fully two-footed, very rare), by level (GAME: FIFA 23 top divisions, overall
# <60 / 60-72 / 78+; better players are more two-footed).
WEAK_FOOT_STARS_WEIGHTS: Dict[str, Dict[int, float]] = {
    "weaker": {1: 0.020, 2: 0.286, 3: 0.624, 4: 0.063, 5: 0.008},
    "normal": {1: 0.009, 2: 0.218, 3: 0.630, 4: 0.130, 5: 0.013},
    "excellent": {1: 0.006, 2: 0.133, 3: 0.478, 4: 0.333, 5: 0.050},
}


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
    # pace and strength: FIFA 23 sprint speed by age against age 24, strength against 29 (MIXED, see above) - young players
    # are faster and weaker than the old curves said; strength keeps growing to about 29
    "pace": [(16, .93), (17, .94), (19, .96), (21, .98), (23, 1.0), (27, .99), (29, .97), (31, .93), (33, .87), (35, .82), (36, .75)],
    "strength": [(16, .72), (17, .75), (19, .81), (21, .87), (23, .93), (25, .96), (27, .98), (29, 1.0), (33, 1.0), (36, .97)],
    "technical": [(16, .80), (19, .90), (23, .97), (26, 1.0), (31, 1.0), (34, .96), (37, .92)],
    "intelligence": [(16, .75), (19, .85), (23, .93), (27, .98), (29, 1.0), (33, 1.02), (36, 1.0)],
    "goalkeeping": [(16, .75), (19, .85), (23, .93), (27, .98), (29, 1.0), (34, 1.0), (37, .95), (40, .88)],
    "personality": [(16, 1.0), (40, 1.0)],
}

STAT_AGE_GROUP: Dict[str, str] = {
    "speed": "pace", "acceleration": "pace",
    "physical_power": "strength", "jumping": "strength", "heading": "technical",  # (heading is a skill: accuracy)
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
