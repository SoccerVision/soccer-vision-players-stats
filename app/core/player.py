import random
import uuid
from typing import Dict, Optional

from app.core.levels.player_config import player_config
from app.core import realism

FIRST_NAMES = ['John', 'Michael', 'David', 'Chris', 'James', 'Robert', 'Daniel', 'William', 'Richard', 'Thomas',
               'Lucas', 'Mateo', 'Luca', 'Noah', 'Leo', 'Omar', 'Yuki', 'Kofi', 'Ivan', 'Diego', 'Elias', 'Andre']
LAST_NAMES = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin',
              'Silva', 'Garcia', 'Rossi', 'Muller', 'Novak', 'Mensah', 'Tanaka', 'Haddad', 'Kowalski', 'Moreau']
DEFAULT_NATIONALITIES = ['CountryA', 'CountryB', 'CountryC']

# Goalkeepers are rated on goalkeeping, not on outfield categories.
GOALKEEPER_EXCLUDED_CATEGORIES = ('attack', 'playmaking', 'defense')


class Player:
    """One generated player.

    All randomness comes from `rng`, so a seeded `random.Random` reproduces the same player.
    Optional arguments pin a property; anything left as None is generated.
    """

    def __init__(self, position: str, level: str = "normal", assigned_numbers: set = None, *,
                 rng: Optional[random.Random] = None, age: Optional[int] = None, side: Optional[str] = None,
                 role: Optional[str] = None, dominant_foot: Optional[str] = None,
                 shirt_number: Optional[int] = None, squad_role: Optional[str] = None,
                 nationalities=None):
        if position not in realism.POSITION_SPECS:
            raise ValueError(f"Unknown position '{position}'")
        level = level.lower()
        if level not in realism.LEVELS:
            raise ValueError(f"Unknown level '{level}'")
        self.rng = rng or random.Random()
        self.position = position
        self.level = level
        self.spec = realism.POSITION_SPECS[position]
        self.squad_role = squad_role
        self.id = str(uuid.UUID(int=self.rng.getrandbits(128), version=4))
        self.name = self.assign_name()
        self.shirt_number = shirt_number if shirt_number is not None else self.assign_shirt_number(assigned_numbers)
        self.age = age if age is not None else self.assign_age()
        self.side = self.assign_side(side)
        self.role = self.assign_role(role)
        self.height = self.assign_height()
        self.preferred_foot = self.assign_preferred_foot(dominant_foot)
        self.weak_foot_stars = self.preferred_foot['weak_foot_stars']
        self.fitness = self.assign_fitness()
        self.stamina = self.assign_stamina()
        self.nationality = self.rng.choice(list(nationalities or DEFAULT_NATIONALITIES))
        self.stat_config = self.get_stat_config()
        self.stats = self.generate_stats()
        self.averages = self.calculate_averages()
        self.overall = self.calculate_overall()
        self.potential = self.calculate_potential()

    # ---------- identity ----------
    def assign_name(self) -> str:
        return f"{self.rng.choice(FIRST_NAMES)} {self.rng.choice(LAST_NAMES)}"

    def assign_shirt_number(self, assigned_numbers: set = None) -> int:
        # Picks a free number but does not reserve it: the squad builder reserves it on accept.
        available = sorted(set(range(1, 100)) - (assigned_numbers or set()))
        if not available:
            raise ValueError("No free shirt numbers left (1-99)")
        return self.rng.choice(available)

    def assign_age(self) -> int:
        return self.rng.randint(21, 30)

    def assign_side(self, side: Optional[str]) -> str:
        if side is not None:
            if side not in self.spec.sides:
                raise ValueError(f"A {self.position} cannot play side '{side}' (allowed: {self.spec.sides})")
            return side
        return self.rng.choice(self.spec.sides)

    def assign_role(self, role: Optional[str]) -> str:
        if role is not None:
            if role not in self.spec.roles:
                raise ValueError(f"Unknown role '{role}' for {self.position} (allowed: {self.spec.roles})")
            return role
        return self.rng.choice(self.spec.roles)

    # ---------- body ----------
    def assign_height(self) -> int:
        mean, std_dev, low, high = self.spec.height
        return round(self.truncated_gauss(mean, std_dev, low, high))

    def assign_preferred_foot(self, dominant_foot: Optional[str] = None) -> Dict:
        if dominant_foot is None:
            p_left = realism.LEFT_FOOT_BY_ROLE.get(self.role, self.spec.left_foot[self.side]) \
                if self.position == "midfielder" else self.spec.left_foot[self.side]
            dominant_foot = "Left" if self.rng.random() < p_left else "Right"
        elif dominant_foot not in ("Left", "Right"):
            raise ValueError("dominant_foot must be 'Left' or 'Right'")
        stars_weights = realism.WEAK_FOOT_STARS_WEIGHTS[self.level]  # (better players are more two-footed)
        stars = self.rng.choices(list(stars_weights), weights=list(stars_weights.values()), k=1)[0]
        return {
            'dominant_foot': dominant_foot,
            'weak_foot_level': realism.legacy_weak_foot_level(stars),
            'weak_foot_stars': stars,
        }

    def assign_fitness(self) -> str:
        return self.rng.choices(['Low', 'Moderate', 'Peak'], weights=[10, 80, 10], k=1)[0]

    def assign_stamina(self) -> int:
        stamina = self.truncated_gauss(70, 10, 50, 90)
        stamina *= realism._interpolate(realism.STAMINA_BY_AGE, self.age)  # (young players build it, older ones lose it)
        stamina += {'Low': -8, 'Moderate': 0, 'Peak': 5}[self.fitness]
        return round(max(30, min(99, stamina)))

    # ---------- stats ----------
    def get_stat_config(self) -> Dict:
        config = player_config['positions'][self.level][self.position]
        if self.position == 'goalkeeper':
            return {k: v for k, v in config.items() if k not in GOALKEEPER_EXCLUDED_CATEGORIES}
        return config

    def truncated_gauss(self, mean, std_dev, min_value=1, max_value=99, max_attempts=50) -> float:
        # Rejection sampling with a clamp fallback, so a bad config can never hang
        for _ in range(max_attempts):
            value = self.rng.gauss(mean, std_dev)
            if min_value <= value <= max_value:
                return value
        return max(min_value, min(max_value, mean))

    def generate_stat(self, mean, std_dev, min_value=1, max_value=99) -> int:
        return round(self.truncated_gauss(mean, std_dev, min_value, max_value))

    def generate_stats(self) -> Dict[str, Dict[str, int]]:
        stats: Dict[str, Dict[str, float]] = {}
        for category, stat_params in self.stat_config.items():
            stats[category] = {}
            for stat_name, params in stat_params.items():
                mean = self.rng.randint(*params['range']) if 'range' in params else params['mean']
                stats[category][stat_name] = self.generate_stat(
                    mean, params.get('std_dev', 4), params.get('min', 1), params.get('max', 99))
        # Heading is a skill (accuracy), not a jump: its own level by position (realism.HEADING_BY_LEVEL); jumping is athletic
        stats['athletic']['heading'] = self.generate_stat(realism.HEADING_BY_LEVEL[self.position][self.level], 6)
        # Aggression belongs to the position, not to the level (a centre-back is more aggressive than a winger)
        stats['mental']['aggression'] = self.generate_stat(realism.AGGRESSION_BY_POSITION[self.position], 12, 10, 95)

        self.apply_role(stats)
        self.apply_age_curve(stats)
        self.apply_fitness(stats)
        self.apply_height(stats)
        self.apply_set_piece_correlation(stats)

        return {category: {name: int(max(1, min(99, round(value)))) for name, value in values.items()}
                for category, values in stats.items()}

    def apply_role(self, stats):
        for key, delta in realism.ROLE_MODIFIERS[self.position][self.role].items():
            category, _, stat = key.partition('.')
            if category not in stats:
                continue
            targets = [stat] if stat else list(stats[category])
            for name in targets:
                if name in stats[category]:
                    stats[category][name] += delta

    def apply_age_curve(self, stats):
        for category, values in stats.items():
            for name in values:
                values[name] *= realism.age_factor(category, name, self.age)

    def apply_fitness(self, stats):
        # Fitness is about the body: it changes athletic attributes only
        multiplier = {'Low': 0.93, 'Moderate': 1.0, 'Peak': 1.04}[self.fitness]
        for name in stats['athletic']:
            stats['athletic'][name] *= multiplier

    def apply_height(self, stats):
        # Relative to the position's average height (MIXED: FIFA 23 players 12 cm apart in the same position - strength +12 to +19,
        # acceleration -8 to -14, sprint speed 0 to -9; jumping, heading and dribbling about the same): a taller player is stronger
        # and a little slower to get going. Jumping is athletic (it can be trained) and heading is a skill - height changes neither.
        athletic = stats['athletic']
        cm = max(-12.0, min(12.0, self.height - self.spec.height[0]))
        athletic['physical_power'] += 1.25 * cm
        athletic['acceleration'] -= 0.9 * cm
        athletic['speed'] -= 0.4 * cm

    def apply_set_piece_correlation(self, stats):
        attack, playmaking, set_pieces = stats.get('attack', {}), stats.get('playmaking', {}), stats.get('set_pieces')
        if not set_pieces or not attack:
            return
        threshold = realism.SET_PIECE_THRESHOLD[self.level]
        if max(attack.get('finishing', 0), attack.get('off_the_ball', 0)) > threshold:
            set_pieces['penalty'] += 5
        if max(attack.get('long_shots', 0), playmaking.get('passing', 0)) > threshold:
            set_pieces['free_kicks'] += 5

    # ---------- summaries ----------
    def calculate_averages(self) -> Dict[str, int]:
        return {category: round(sum(values.values()) / len(values)) for category, values in self.stats.items()}

    def calculate_overall(self) -> int:
        total = weight_sum = 0.0
        for key, weight in realism.OVERALL_WEIGHTS[self.position].items():
            category, _, stat = key.partition('.')
            value = self.stats.get(category, {}).get(stat)
            if value is not None:
                total += value * weight
                weight_sum += weight
        return round(total / weight_sum)

    def calculate_potential(self) -> Optional[int]:
        # Only young players have meaningful growth ahead of them
        if self.age > 23:
            return None
        growth = (27 - self.age) * self.rng.uniform(1.0, 3.0)
        return int(min(99, round(self.overall + growth)))

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'shirt_number': self.shirt_number,
            'position': self.position,
            'level': self.level.capitalize(),
            'age': self.age,
            'height': self.height,
            'preferred_foot': self.preferred_foot,
            'stamina': self.stamina,
            'fitness': self.fitness,
            'nationality': self.nationality,
            'stats': self.stats,
            'averages': self.averages,
            # v2 additions (v1 clients can ignore them)
            'side': self.side,
            'role': self.role,
            'overall': self.overall,
            'potential': self.potential,
            'weak_foot_stars': self.weak_foot_stars,
            'squad_role': self.squad_role,
        }
