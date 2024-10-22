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
        if random.random() < 0.01:  # 1% chance for ambidextrous
            weaker_foot_level = 3
        else:
            weaker_foot_level = random.choices(
                [1, 2],
                weights=[70, 30],
                k=1
            )[0]
        return {
            'Dominant Foot': dominant_foot,
            'Weak Foot Level': weaker_foot_level
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
        athletic_stats = player_stats['Athletic']

        if 'Heading' not in athletic_stats:
            athletic_stats['Heading'] = self.generate_stat(athletic_stats['Jumping'], 4)

        if self.height > 185:
            increase_percentage = random.uniform(0.10, 0.12)
            athletic_stats['Jumping'] = self.cap_stat(round(athletic_stats['Jumping'] * (1 + increase_percentage)))
            athletic_stats['Heading'] = self.cap_stat(round(athletic_stats['Heading'] * (1 + increase_percentage)))

            height_diff = self.height - 181
            adjustment = int(height_diff / 3)
            adjustment = self.cap_stat(max(-5, min(5, adjustment)), 99)
            athletic_stats['Physical Power'] += adjustment

            athletic_stats['Speed'] -= adjustment
            athletic_stats['Acceleration'] -= adjustment
        else:
            height_diff = self.height - 181
            adjustment = int(height_diff / 3)
            adjustment = self.cap_stat(max(-5, min(5, adjustment)), 99)
            if adjustment != 0:
                athletic_stats['Jumping'] += adjustment
                athletic_stats['Heading'] += adjustment
                athletic_stats['Physical Power'] += adjustment
                athletic_stats['Speed'] -= adjustment
                athletic_stats['Acceleration'] -= adjustment
            if adjustment < 0 and self.position not in ['Defender', 'Goalkeeper', 'Fullback']:
                athletic_stats['Dribbling'] -= adjustment

        for stat in athletic_stats:
            athletic_stats[stat] = self.cap_stat(max(1, min(99, athletic_stats.get(stat, 50))), 99)

    def apply_preferred_foot_adjustments(self, player_stats):
        weak_foot_level = self.preferred_foot['Weak Foot Level']
        if weak_foot_level == 3:
            if 'Attack' in player_stats:
                player_stats['Attack']['Finishing'] = self.cap_stat(player_stats['Attack'].get('Finishing', 0) + 5, 99)
                player_stats['Attack']['Long Shots'] = self.cap_stat(player_stats['Attack'].get('Long Shots', 0) + 5,
                                                                     99)
            if 'Athletic' in player_stats:
                player_stats['Athletic']['Dribbling'] = self.cap_stat(player_stats['Athletic'].get('Dribbling', 0) + 5,
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

        athletic_stats = player_stats['Athletic']
        athletic_stats['Heading'] = self.generate_stat(athletic_stats['Jumping'], 4)

        self._balance_athletic_stats(athletic_stats, config)
        self._adjust_physical_power(athletic_stats, config)
        self._correlate_set_pieces(player_stats, config)

    def _balance_athletic_stats(self, athletic_stats, config):
        speed_stats = [
            athletic_stats.get('Speed', config['default']),
            athletic_stats.get('Acceleration', config['default']),
            athletic_stats.get('Dribbling', config['default'])
        ]
        heading_stats = [
            athletic_stats.get('Jumping', config['default']),
            athletic_stats.get('Heading', config['default'])
        ]

        if all(stat < config['threshold'] for stat in speed_stats):
            athletic_stats['Jumping'] = self.cap_stat(max(athletic_stats['Jumping'], config['jumping_adjustment']), 99)
            athletic_stats['Heading'] = self.cap_stat(max(athletic_stats['Heading'], config['heading_adjustment']), 99)
        elif all(stat < config['threshold'] for stat in heading_stats):
            athletic_stats['Speed'] = self.cap_stat(max(athletic_stats['Speed'], config['speed_adjustment']), 99)
            athletic_stats['Acceleration'] = self.cap_stat(
                max(athletic_stats['Acceleration'], config['speed_adjustment']), 99)
            if self.position not in ['Defender', 'Goalkeeper', 'Fullback']:
                athletic_stats['Dribbling'] = self.cap_stat(
                    max(athletic_stats['Dribbling'], config['dribbling_non_defender']), 99)
            else:
                athletic_stats['Dribbling'] = self.cap_stat(
                    max(athletic_stats['Dribbling'], config['dribbling_defender']), 99)

    def _adjust_physical_power(self, athletic_stats, config):
        if athletic_stats['Jumping'] > config['physical_power_threshold']:
            athletic_stats['Physical Power'] = self.cap_stat(
                max(athletic_stats['Physical Power'], config['physical_power_threshold']), 99)

        if athletic_stats['Acceleration'] < config['physical_power_threshold'] or athletic_stats['Speed'] < config[
            'physical_power_threshold']:
            athletic_stats['Physical Power'] = self.cap_stat(self.generate_stat(config['physical_power_stat'], 4), 99)

    def _correlate_set_pieces(self, player_stats, config):
        attack_stats = player_stats.get('Attack', {})
        playmaking_stats = player_stats.get('Playmaking', {})
        set_pieces = player_stats.get('Set Pieces', {})

        if attack_stats and set_pieces:
            if attack_stats.get('Finishing', 0) > config['finishing_threshold'] or attack_stats.get('Off The Ball', 0) > \
                    config['finishing_threshold']:
                if 'Penalty' in set_pieces:
                    set_pieces['Penalty'] = self.cap_stat(set_pieces['Penalty'] + config['set_pieces_increment'], 99)

            if attack_stats.get('Long Shots', 0) > config['finishing_threshold'] or playmaking_stats.get('Passing', 0) > \
                    config['finishing_threshold']:
                if 'Free Kicks' in set_pieces:
                    set_pieces['Free Kicks'] = self.cap_stat(set_pieces['Free Kicks'] + config['set_pieces_increment'],
                                                             99)

    def calculate_averages(self):
        averages = {}
        for category, stats in self.stats.items():
            avg = sum(stats.values()) / len(stats)
            averages[category] = round(avg)
        return averages

    def to_dict(self):
        return {
            'Name': self.name,
            'Shirt_Number': self.shirt_number,
            'Position': self.position,
            "Level": self.level.capitalize(),
            'Age': self.age,
            'Height': self.height,
            'Preferred_Foot': self.preferred_foot,
            'Stamina': self.stamina,
            'Fitness': self.fitness,
            'Nationality': self.nationality,
            'Stats': self.stats,
            'Averages': self.averages,
            'ID': self.id
        }
