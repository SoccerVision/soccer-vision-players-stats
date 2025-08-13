import random
import uuid
from app.core.levels.player_config import player_config


class Player:
    def __init__(self, position, level="normal", assigned_numbers: set = None):
        self.position = position
        self.level = level
        self.id = self.assign_id()
        self.name = self.assign_name()
        self.shirt_number = self.assign_shirt_number(assigned_numbers)
        self.age = self.assign_age()
        self.height = self.assign_height()
        self.preferred_foot = self.assign_preferred_foot()
        self.stamina = self.assign_stamina()
        self.fitness = self.assign_fitness()
        self.nationality = self.assign_nationality()
        self.stat_config = self.get_stat_config()
        self.stats = self.generate_stats()
        self.averages = self.calculate_averages()

    # Assign unique ID to each player
    def assign_id(self) -> str:
        return str(uuid.uuid4())

    # Cap a value to a maximum of 99
    def cap_stat(self, value, max_value=99):
        return min(value, max_value)

    # Generate a random name for the player
    def assign_name(self) -> str:
        first_names = ['John', 'Michael', 'David', 'Chris', 'James', 'Robert', 'Daniel', 'William', 'Richard', 'Thomas']
        last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris',
                      'Martin']
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    # Assign a unique shirt number to each player
    def assign_shirt_number(self, assigned_numbers: set = None) -> int:
        if assigned_numbers is None:
            assigned_numbers = set()
        available_numbers = set(range(1, 100)) - assigned_numbers
        while not available_numbers:
            # If there are no available numbers, expand the range
            max_number = max(assigned_numbers) + 1 if assigned_numbers else 100
            available_numbers = set(range(1, max_number)) - assigned_numbers

        shirt_number = random.choice(list(available_numbers))
        assigned_numbers.add(shirt_number)
        return shirt_number

    def assign_age(self) -> int:
        return random.randint(21, 30)

    def assign_height(self):
        # Generate height with normal distribution centered at 183 cm
        while True:
            height = random.gauss(178, 8)
            if 160 <= height <= 200:
                if height < 160 or height > 190:
                    if random.random() < 0.10:  # 10% chance
                        return round(height)
                else:
                    return round(height)

    def assign_preferred_foot(self):
        # Assign dominant foot with updated probabilities
        dominant_foot = random.choices(
            ['Right', 'Left'],
            weights=[75, 25],  # 75% Right-footed, 25% Left-footed
            k=1
        )[0]
        # Weaker foot level
        if random.random() < 0.1:  # 10% chance for ambidextrous
            weaker_foot_level = 3
        else:
            weaker_foot_level = random.choices(
                [1, 2],
                weights=[70, 30],
                k=1
            )[0]
        return {
            'dominant_foot': dominant_foot,
            'weak_foot_level': weaker_foot_level
        }

    def assign_stamina(self):
        base_stamina = random.gauss(70, 10)
        base_stamina = max(50, min(90, base_stamina))
        # Adjust for age
        if self.age >= 29:
            base_stamina -= 5
        return round(base_stamina)

    def assign_fitness(self):
        fitness_level = random.choices(
            ['Low', 'Moderate', 'Peak'],
            weights=[10, 80, 10],
            k=1
        )[0]
        return fitness_level

    def assign_nationality(self) -> str:
        countries = ['CountryA', 'CountryB', 'CountryC']  # Placeholder list
        return random.choice(countries)

    def get_stat_config(self):
        return player_config['positions'][self.level.lower()].get(self.position, {})

    def generate_stat(self, mean, std_dev, min_value=0, max_value=99):
        while True:
            value = random.gauss(mean, std_dev)
            if min_value <= value <= max_value:
                return round(value)

    def generate_stats(self):
        player_stats = {}
        default_mean_by_level = {
            'weaker': 35,
            'normal': 50,
            'excellent': 70
        }

        default_mean = default_mean_by_level.get(self.level, 50)
        for category, stats in self.stat_config.items():
            category_stats = {}
            for stat_name, params in stats.items():
                mean = params.get('mean', default_mean)
                std_dev = params.get('std_dev', 4)
                min_value = params.get('min', 0)
                max_value = params.get('max', 99)
                stat_value = self.generate_stat(mean, std_dev, min_value, max_value)
                category_stats[stat_name] = self.cap_stat(stat_value, max_value=99)
            player_stats[category] = category_stats

        self.apply_age_adjustments(player_stats)
        self.apply_fitness_adjustments(player_stats)
        self.apply_height_adjustments(player_stats)
        self.apply_preferred_foot_adjustments(player_stats)
        self.additional_calculations(player_stats)

        for category in player_stats:
            for stat_name in player_stats[category]:
                player_stats[category][stat_name] = self.cap_stat(player_stats[category][stat_name], 99)
        return player_stats

    def apply_age_adjustments(self, player_stats):
        if self.age <= 24:
            multiplier = random.uniform(0.95, 0.98)
        elif self.age >= 29:
            multiplier = random.uniform(0.97, 0.99)
        else:
            multiplier = 1.0

        for category in player_stats:
            for stat in player_stats[category]:
                player_stats[category][stat] = self.cap_stat(round(player_stats[category][stat] * multiplier), 99)

    def apply_fitness_adjustments(self, player_stats):
        if self.fitness == 'Low':
            multiplier = 0.9
        elif self.fitness == 'Peak':
            multiplier = 1.05
        else:
            multiplier = 1.0

        for category in player_stats:
            for stat in player_stats[category]:
                if stat != 'Stamina':
                    player_stats[category][stat] = self.cap_stat(round(player_stats[category][stat] * multiplier), 99)

    def apply_height_adjustments(self, player_stats):
        athletic_stats = player_stats['athletic']

        if 'heading' not in athletic_stats:
            athletic_stats['heading'] = self.generate_stat(athletic_stats['jumping'], 4)

        if self.height > 185:
            increase_percentage = random.uniform(0.10, 0.12)
            athletic_stats['jumping'] = self.cap_stat(round(athletic_stats['jumping'] * (1 + increase_percentage)))
            athletic_stats['heading'] = self.cap_stat(round(athletic_stats['heading'] * (1 + increase_percentage)))

            height_diff = self.height - 181
            adjustment = int(height_diff / 3)
            adjustment = self.cap_stat(max(-5, min(5, adjustment)), 99)
            athletic_stats['physical_power'] += adjustment

            athletic_stats['speed'] -= adjustment
            athletic_stats['acceleration'] -= adjustment
        else:
            height_diff = self.height - 181
            adjustment = int(height_diff / 3)
            adjustment = self.cap_stat(max(-5, min(5, adjustment)), 99)
            if adjustment != 0:
                athletic_stats['jumping'] += adjustment
                athletic_stats['heading'] += adjustment
                athletic_stats['physical_power'] += adjustment
                athletic_stats['speed'] -= adjustment
                athletic_stats['acceleration'] -= adjustment
            if adjustment < 0 and self.position not in ['defender', 'goalkeeper', 'fullback']:
                athletic_stats['dribbling'] -= adjustment

        for stat in athletic_stats:
            athletic_stats[stat] = self.cap_stat(max(1, min(99, athletic_stats.get(stat, 50))), 99)

    def apply_preferred_foot_adjustments(self, player_stats):
        weak_foot_level = self.preferred_foot['weak_foot_level']
        if weak_foot_level == 3:
            if 'attack' in player_stats:
                player_stats['attack']['finishing'] = self.cap_stat(player_stats['attack'].get('finishing', 0) + 5, 99)
                player_stats['attack']['long_shots'] = self.cap_stat(player_stats['attack'].get('long_shots', 0) + 5,
                                                                     99)
            if 'athletic' in player_stats:
                player_stats['athletic']['dribbling'] = self.cap_stat(player_stats['athletic'].get('dribbling', 0) + 5,
                                                                      99)

    def additional_calculations(self, player_stats):
        LEVEL_CONFIG = {
            'weaker': {
                'default': 35,
                'threshold': 55,
                'jumping_adjustment': 50,
                'heading_adjustment': 50,
                'speed_adjustment': 50,
                'dribbling_non_defender': 45,
                'dribbling_defender': 40,
                'physical_power_threshold': 50,
                'physical_power_stat': 55,
                'finishing_threshold': 55,
                'set_pieces_increment': 5
            },
            'normal': {
                'default': 50,
                'threshold': 70,
                'jumping_adjustment': 65,
                'heading_adjustment': 65,
                'speed_adjustment': 65,
                'dribbling_non_defender': 60,
                'dribbling_defender': 55,
                'physical_power_threshold': 65,
                'physical_power_stat': 70,
                'finishing_threshold': 70,
                'set_pieces_increment': 5
            },
            'excellent': {
                'default': 70,
                'threshold': 90,
                'jumping_adjustment': 85,
                'heading_adjustment': 85,
                'speed_adjustment': 85,
                'dribbling_non_defender': 80,
                'dribbling_defender': 75,
                'physical_power_threshold': 85,
                'physical_power_stat': 90,
                'finishing_threshold': 90,
                'set_pieces_increment': 5
            }
        }
        config = LEVEL_CONFIG.get(self.level.lower(), LEVEL_CONFIG['normal'])

        athletic_stats = player_stats['athletic']
        athletic_stats['heading'] = self.generate_stat(athletic_stats['jumping'], 4)

        self._balance_athletic_stats(athletic_stats, config)
        self._adjust_physical_power(athletic_stats, config)
        self._correlate_set_pieces(player_stats, config)

    def _balance_athletic_stats(self, athletic_stats, config):
        speed_stats = [
            athletic_stats.get('speed', config['default']),
            athletic_stats.get('acceleration', config['default']),
            athletic_stats.get('dribbling', config['default'])
        ]
        heading_stats = [
            athletic_stats.get('jumping', config['default']),
            athletic_stats.get('heading', config['default'])
        ]

        if all(stat < config['threshold'] for stat in speed_stats):
            athletic_stats['jumping'] = self.cap_stat(max(athletic_stats['jumping'], config['jumping_adjustment']), 99)
            athletic_stats['heading'] = self.cap_stat(max(athletic_stats['heading'], config['heading_adjustment']), 99)
        elif all(stat < config['threshold'] for stat in heading_stats):
            athletic_stats['speed'] = self.cap_stat(max(athletic_stats['speed'], config['speed_adjustment']), 99)
            athletic_stats['acceleration'] = self.cap_stat(
                max(athletic_stats['acceleration'], config['speed_adjustment']), 99)
            if self.position not in ['defender', 'goalkeeper', 'fullback']:
                athletic_stats['dribbling'] = self.cap_stat(
                    max(athletic_stats['dribbling'], config['dribbling_non_defender']), 99)
            else:
                athletic_stats['dribbling'] = self.cap_stat(
                    max(athletic_stats['dribbling'], config['dribbling_defender']), 99)

    def _adjust_physical_power(self, athletic_stats, config):
        if athletic_stats['jumping'] > config['physical_power_threshold']:
            athletic_stats['physical_power'] = self.cap_stat(
                max(athletic_stats['physical_power'], config['physical_power_threshold']), 99)

        if athletic_stats['acceleration'] < config['physical_power_threshold'] or athletic_stats['speed'] < config[
            'physical_power_threshold']:
            athletic_stats['physical_power'] = self.cap_stat(self.generate_stat(config['physical_power_stat'], 4), 99)

    def _correlate_set_pieces(self, player_stats, config):
        attack_stats = player_stats.get('attack', {})
        playmaking_stats = player_stats.get('playmaking', {})
        set_pieces = player_stats.get('set_pieces', {})

        if attack_stats and set_pieces:
            if attack_stats.get('finishing', 0) > config['finishing_threshold'] or attack_stats.get('off_the_ball', 0) > \
                    config['finishing_threshold']:
                if 'penalty' in set_pieces:
                    set_pieces['penalty'] = self.cap_stat(set_pieces['penalty'] + config['set_pieces_increment'], 99)

            if attack_stats.get('long_shots', 0) > config['finishing_threshold'] or playmaking_stats.get('passing', 0) > \
                    config['finishing_threshold']:
                if 'free_kicks' in set_pieces:
                    set_pieces['free_kicks'] = self.cap_stat(set_pieces['free_kicks'] + config['set_pieces_increment'],
                                                             99)

    def calculate_averages(self):
        averages = {}
        for category, stats in self.stats.items():
            avg = sum(stats.values()) / len(stats)
            averages[category] = round(avg)
        return averages

    def to_dict(self):
        return {
            'name': self.name,
            'shirt_number': self.shirt_number,
            'position': self.position,
            "level": self.level.capitalize(),
            'age': self.age,
            'height': self.height,
            'preferred_foot': self.preferred_foot,
            'stamina': self.stamina,
            'fitness': self.fitness,
            'nationality': self.nationality,
            'stats': self.stats,
            'averages': self.averages,
            'id': self.id
        }
