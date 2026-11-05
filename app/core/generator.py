"""One seeded generator for every kind of squad.

Everything random flows from a single `random.Random(seed)`, so the same options + seed
always return the same squad (names, ids, numbers and stats included).
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from app.core import realism
from app.core.player import Player

MAX_SQUAD_SIZE = 60
DEFAULT_MIXED_WEIGHTS: Dict[str, float] = {"excellent": 1, "weaker": 5, "normal": 44}  # v1 odds: 2% / 10% / 88%

# name -> (min_age, max_age, mode). mode=None means uniform, REAL_AGES the real age spread (realism.AGE_HISTOGRAM),
# otherwise triangular around mode.
REAL_AGES = 0
AGE_PROFILES: Dict[str, Tuple[int, int, Optional[int]]] = {
    "realistic": (16, 40, REAL_AGES),  # the age spread of real first-team squads (FIFA 23 top divisions: 18% aged 21 or under, 6% 34+)
    "youth": (16, 19, None),
    "young": (18, 23, None),
    "prime": (24, 29, None),
    "veteran": (30, 35, None),
    "legacy": (21, 30, None),   # v1 behaviour
}


@dataclass(frozen=True)
class Slot:
    position: str
    side: Optional[str] = None
    role: Optional[str] = None
    dominant_foot: Optional[str] = None
    age_range: Optional[Tuple[int, int]] = None
    squad_role: Optional[str] = None


def _xi(*slots: Tuple) -> List[Slot]:
    return [Slot(*s) for s in slots]


GK, CB, FB, MF, W, ST = "goalkeeper", "defender", "fullback", "midfielder", "winger", "striker"

FORMATIONS: Dict[str, List[Slot]] = {
    "4-4-2": _xi((GK,), (FB, "L"), (CB, "L"), (CB, "R"), (FB, "R"), (W, "L", "traditional"),
                 (MF, "C", "box_to_box"), (MF, "C", "playmaker"), (W, "R", "traditional"),
                 (ST, "C", "target_man"), (ST, "C", "poacher")),
    "4-3-3": _xi((GK,), (FB, "L"), (CB, "L"), (CB, "R"), (FB, "R"), (MF, "C", "defensive_mid"),
                 (MF, "C", "box_to_box"), (MF, "C", "playmaker"), (W, "L", "inside_forward"),
                 (W, "R", "inside_forward"), (ST, "C", "complete_forward")),
    "4-2-3-1": _xi((GK,), (FB, "L"), (CB, "L"), (CB, "R"), (FB, "R"), (MF, "C", "defensive_mid"),
                   (MF, "C", "box_to_box"), (W, "L"), (MF, "C", "attacking_mid"), (W, "R"), (ST,)),
    "3-5-2": _xi((GK,), (CB, "L"), (CB, "C"), (CB, "R"), (FB, "L", "wing_back"), (MF, "C", "defensive_mid"),
                 (MF, "C", "box_to_box"), (MF, "C", "playmaker"), (FB, "R", "wing_back"), (ST,), (ST,)),
    "3-4-3": _xi((GK,), (CB, "L"), (CB, "C"), (CB, "R"), (FB, "L", "wing_back"), (MF, "C", "defensive_mid"),
                 (MF, "C", "box_to_box"), (FB, "R", "wing_back"), (W, "L"), (ST,), (W, "R")),
    "5-3-2": _xi((GK,), (FB, "L", "wing_back"), (CB, "L"), (CB, "C"), (CB, "R"), (FB, "R", "wing_back"),
                 (MF, "C", "defensive_mid"), (MF, "C", "box_to_box"), (MF, "C", "playmaker"), (ST,), (ST,)),
}

TEMPLATES: Dict[str, str] = {
    "legacy": "v1 squad of 22: 2 GK, 3 CB, 4 FB, 4 MF, 2 W, 3 ST + 2 young and 2 veteran players",
    "legacy_core": "v1 squad of 18 without the young/veteran extras",
    "youth": "17-player academy squad: 2 GK, 3 CB, 3 FB, 4 MF, 2 W, 3 ST",
    "uefa25": "25-player competition squad: 3 GK, 4 CB, 4 FB, 7 MF, 4 W, 3 ST",
    "formation": "23 players: a starting XI for `formation`, a full backup XI and a third goalkeeper",
}


def _alternate_sides(position: str, count: int) -> List[Slot]:
    sides = realism.POSITION_SPECS[position].sides
    if sides == ("C",):
        return [Slot(position) for _ in range(count)]
    order = ["L", "R"] + (["C"] if "C" in sides else [])
    return [Slot(position, order[i % len(order)]) for i in range(count)]


def _legacy_core() -> List[Slot]:
    return ([Slot(GK)] * 2 + [Slot(CB, "L"), Slot(CB, "C"), Slot(CB, "R")]
            + [Slot(FB, "L", dominant_foot="Left"), Slot(FB, "R", dominant_foot="Right"), Slot(FB), Slot(FB)]
            + [Slot(ST)] * 3 + [Slot(W, "L"), Slot(W, "R")] + [Slot(MF)] * 4)


def build_slots(template: str, formation: Optional[str], positions: Optional[Dict[str, int]],
                rng: random.Random) -> List[Slot]:
    if positions:
        unknown = set(positions) - set(realism.POSITIONS)
        if unknown:
            raise ValueError(f"Unknown positions: {sorted(unknown)}")
        if any(c < 0 for c in positions.values()):
            raise ValueError("Position counts must be >= 0")
        total = sum(positions.values())
        if total > MAX_SQUAD_SIZE:
            raise ValueError(f"Squad too large ({total}); max is {MAX_SQUAD_SIZE}")
        return [slot for pos in realism.POSITIONS for slot in _alternate_sides(pos, positions.get(pos, 0))]
    if template == "formation" or formation:
        name = formation or "4-3-3"
        if name not in FORMATIONS:
            raise ValueError(f"Unknown formation '{name}' (allowed: {sorted(FORMATIONS)})")
        xi = FORMATIONS[name]
        starters = [Slot(s.position, s.side, s.role, squad_role="starter") for s in xi]
        bench = [Slot(s.position, s.side, s.role, squad_role="bench") for s in xi]
        return starters + bench + [Slot(GK, squad_role="bench")]
    if template == "legacy":
        extras = [Slot(rng.choice(realism.POSITIONS), age_range=(18, 21)) for _ in range(2)]
        extras += [Slot(rng.choice(realism.POSITIONS), age_range=(29, 33)) for _ in range(2)]
        return _legacy_core() + extras
    if template == "legacy_core":
        return _legacy_core()
    if template == "youth":
        return ([Slot(GK)] * 2 + _alternate_sides(CB, 3) + _alternate_sides(FB, 3) + [Slot(ST)] * 3
                + _alternate_sides(W, 2) + [Slot(MF)] * 4)
    if template == "uefa25":
        return ([Slot(GK)] * 3 + _alternate_sides(CB, 4) + _alternate_sides(FB, 4) + [Slot(MF)] * 7
                + _alternate_sides(W, 4) + [Slot(ST)] * 3)
    raise ValueError(f"Unknown template '{template}' (allowed: {sorted(TEMPLATES)})")


@dataclass
class GenerationOptions:
    level: str = "normal"                   # weaker | normal | excellent | mixed
    level_weights: Optional[Dict[str, float]] = None  # only for level="mixed"
    age_profile: str = "realistic"
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    template: str = "uefa25"
    formation: Optional[str] = None
    positions: Optional[Dict[str, int]] = None  # custom counts, overrides template/formation
    nationalities: Optional[List[str]] = None
    seed: Optional[int] = None


@dataclass
class Squad:
    seed: int
    options: GenerationOptions
    players: List[Player] = field(default_factory=list)


def new_seed() -> int:
    return random.SystemRandom().randrange(2 ** 31)


def pick_level(rng: random.Random, options: GenerationOptions) -> str:
    if options.level != "mixed":
        if options.level not in realism.LEVELS:
            raise ValueError(f"Unknown level '{options.level}'")
        return options.level
    weights = options.level_weights or DEFAULT_MIXED_WEIGHTS
    if set(weights) - set(realism.LEVELS) or sum(weights.values()) <= 0 or min(weights.values()) < 0:
        raise ValueError("level_weights must use weaker/normal/excellent with non-negative weights")
    return rng.choices(list(weights), weights=list(weights.values()), k=1)[0]


def age_bounds(options: GenerationOptions, slot: Optional[Slot] = None):
    if options.age_profile not in AGE_PROFILES:
        raise ValueError(f"Unknown age_profile '{options.age_profile}' (allowed: {sorted(AGE_PROFILES)})")
    low, high, mode = AGE_PROFILES[options.age_profile]
    if slot is not None and slot.age_range:
        low, high, mode = slot.age_range[0], slot.age_range[1], None
    else:
        if options.min_age is not None:
            low = options.min_age
        if options.max_age is not None:
            high = options.max_age
    if not 15 <= low <= high <= 45:
        raise ValueError(f"Invalid age range {low}-{high} (allowed 15-45, min <= max)")
    return low, high, mode


def draw_age(rng: random.Random, low: int, high: int, mode: Optional[int]) -> int:
    if mode == REAL_AGES:
        ages = [a for a in realism.AGE_HISTOGRAM if low <= a <= high]
        if ages:
            return rng.choices(ages, weights=[realism.AGE_HISTOGRAM[a] for a in ages], k=1)[0]
        return rng.randint(low, high)
    if mode is None or not low <= mode <= high or low == high:
        return rng.randint(low, high)
    return int(min(high, max(low, round(rng.triangular(low, high, mode)))))


def pick_shirt_number(rng: random.Random, slot: Slot, taken: set) -> int:
    if slot.squad_role != "bench":
        for number in realism.preferred_numbers(slot.position, slot.side, slot.role):
            if number not in taken:
                return number
    free = sorted(set(range(2, 100)) - taken) or sorted(set(range(1, 100)) - taken)
    if not free:
        raise ValueError("No free shirt numbers left (1-99)")
    return rng.choice(free)


def make_player(rng: random.Random, options: GenerationOptions, slot: Slot, taken: set) -> Player:
    level = pick_level(rng, options)
    age = draw_age(rng, *age_bounds(options, slot))
    number = pick_shirt_number(rng, slot, taken)
    taken.add(number)
    return Player(slot.position, level, rng=rng, age=age, side=slot.side, role=slot.role,
                  dominant_foot=slot.dominant_foot, shirt_number=number, squad_role=slot.squad_role,
                  nationalities=options.nationalities)


def generate_squad(options: GenerationOptions) -> Squad:
    seed = options.seed if options.seed is not None else new_seed()
    rng = random.Random(seed)
    slots = build_slots(options.template, options.formation, options.positions, rng)
    if not slots:
        raise ValueError("Squad is empty: ask for at least one player")
    if len(slots) > MAX_SQUAD_SIZE:
        raise ValueError(f"Squad too large ({len(slots)}); max is {MAX_SQUAD_SIZE}")
    taken: set = set()
    players = [make_player(rng, options, slot, taken) for slot in slots]
    return Squad(seed=seed, options=options, players=players)


def generate_players(options: GenerationOptions, count: int, position: Optional[str] = None,
                     side: Optional[str] = None, role: Optional[str] = None,
                     dominant_foot: Optional[str] = None, age: Optional[int] = None) -> Squad:
    """Free agents: `count` players with the same filters (random position when none given)."""
    if not 1 <= count <= MAX_SQUAD_SIZE:
        raise ValueError(f"count must be 1-{MAX_SQUAD_SIZE}")
    seed = options.seed if options.seed is not None else new_seed()
    rng = random.Random(seed)
    taken: set = set()
    players = []
    for _ in range(count):
        slot = Slot(position or rng.choice(realism.POSITIONS), side, role, dominant_foot,
                    age_range=(age, age) if age is not None else None)
        players.append(make_player(rng, options, slot, taken))
    return Squad(seed=seed, options=options, players=players)


def squad_summary(players: List[Player]) -> Dict:
    count = len(players)
    by_position: Dict[str, int] = {}
    for p in players:
        by_position[p.position] = by_position.get(p.position, 0) + 1
    starters = [p for p in players if p.squad_role == "starter"]
    return {
        "count": count,
        "by_position": by_position,
        "average_age": round(sum(p.age for p in players) / count, 1),
        "average_overall": round(sum(p.overall for p in players) / count, 1),
        "starting_xi_overall": round(sum(p.overall for p in starters) / len(starters), 1) if starters else None,
        "left_footed": sum(p.preferred_foot["dominant_foot"] == "Left" for p in players),
    }
