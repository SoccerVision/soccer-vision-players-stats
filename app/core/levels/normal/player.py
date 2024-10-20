import random
import uuid


class Player:
    def __init__(self, position, assigned_numbers: set = None):
        self.position = position
        self.level = 'Normal'
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

    def assign_nationality(self)-> str:
        countries = ['CountryA', 'CountryB', 'CountryC']  # Placeholder list
        return random.choice(countries)

    # Base stat configuration for players
    def get_stat_config(self):
        stat_config = {
            'Mental': {
                'Aggression': {'mean': random.randint(10, 90), 'std_dev': 5},
                'Teamwork': {'mean': 50, 'std_dev': 8},
                'Decisions': {'mean': 50, 'std_dev': 6},
                'Composure': {'mean': 50, 'std_dev': 6},
            },
            'Defense': {
                'Tackling': {'mean': 50, 'std_dev': 4},
                'Marking': {'mean': 50, 'std_dev': 4},
                'Positioning': {'mean': 50, 'std_dev': 4},
            },
            'Attack': {
                'Finishing': {'mean': 50, 'std_dev': 4},
                'Long Shots': {'mean': 50, 'std_dev': 4},
                'Off The Ball': {'mean': 50, 'std_dev': 4},
            },
            'Playmaking': {
                'Creative': {'mean': 50, 'std_dev': 4},
                'Passing': {'mean': 50, 'std_dev': 4},
                'Crossing': {'mean': 50, 'std_dev': 4},
            },
            'Athletic': {
                'Physical Power': {'mean': 55, 'std_dev': 8},
                'Ball Control': {'mean': 60, 'std_dev': 4},
                'Dribbling': {'mean': 60, 'std_dev': 4},
                'Jumping': {'mean': 55, 'std_dev': 8},
                'Acceleration': {'mean': 60, 'std_dev': 8},
                'Speed': {'mean': 60, 'std_dev': 8},
            },
            'Set Pieces': {
                'Free Kicks': {'mean': 50, 'std_dev': 15, 'min': 30, 'max': 90},
                'Penalty': {'mean': 60, 'std_dev': 15, 'min': 30, 'max': 90},
            },
        }
        return stat_config

    def generate_stat(self, mean, std_dev, min_value=0, max_value=99):
        while True:
            value = random.gauss(mean, std_dev)
            if min_value <= value <= max_value:
                return round(value)

    def generate_stats(self):
        player_stats = {}
        for category, stats in self.stat_config.items():
            category_stats = {}
            for stat_name, params in stats.items():
                mean = params.get('mean', 50)
                std_dev = params.get('std_dev', 4)
                min_value = params.get('min', 0)
                max_value = params.get('max', 99)
                stat_value = self.generate_stat(mean, std_dev, min_value, max_value)
                category_stats[stat_name] = stat_value
            player_stats[category] = category_stats

        # Apply age adjustments
        self.apply_age_adjustments(player_stats)
        # Apply fitness adjustments
        self.apply_fitness_adjustments(player_stats)
        # Apply height adjustments
        self.apply_height_adjustments(player_stats)
        # Apply preferred foot adjustments
        self.apply_preferred_foot_adjustments(player_stats)
        # Additional calculations
        self.additional_calculations(player_stats)
        self.adjust_stats_by_level(player_stats)
        return player_stats

    # Adjust player stats based on level (Normal, Weaker, Excellent)
    def adjust_stats_by_level(self, player_stats):
        if self.level == 'Weaker':
            factor = random.uniform(0.7, 0.9)
        elif self.level == 'Excellent':
            factor = random.uniform(1.1, 1.3)
        else:
            factor = 1.0  # Normal

        for category, stats in player_stats.items():
            for stat in stats:
                player_stats[category][stat] = round(player_stats[category][stat] * factor)
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
                player_stats[category][stat] = round(player_stats[category][stat] * multiplier)

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
                    player_stats[category][stat] = round(player_stats[category][stat] * multiplier)

    def adjust_acceleration_based_on_speed(self, player_stats):
        speed = player_stats['Athletic']['Speed']
        acceleration_min = max(1, speed - 10)
        acceleration_max = min(99, speed + 10)
        player_stats['Athletic']['Acceleration'] = random.randint(acceleration_min, acceleration_max)

    def apply_height_adjustments(self, player_stats):
        athletic_stats = player_stats['Athletic']

        # Ensure 'Heading' stat is generated based on 'Jumping' before adjustments
        if 'Heading' not in athletic_stats:
            athletic_stats['Heading'] = self.generate_stat(athletic_stats['Jumping'], 4)

        if self.height > 185:
            # Increase Jumping and Heading by 10%-12%
            increase_percentage = random.uniform(0.10, 0.12)
            athletic_stats['Jumping'] = round(athletic_stats['Jumping'] * (1 + increase_percentage))
            athletic_stats['Heading'] = round(athletic_stats['Heading'] * (1 + increase_percentage))

            # Adjust Physical Power, Speed, Acceleration based on height difference
            height_diff = self.height - 181
            adjustment = int(height_diff / 3)
            adjustment = max(-5, min(5, adjustment))
            athletic_stats['Physical Power'] += adjustment


            athletic_stats['Speed'] -= adjustment
            athletic_stats['Acceleration'] -= adjustment

        else:
            # Existing adjustment based on height difference
            height_diff = self.height - 181
            adjustment = int(height_diff / 3)
            adjustment = max(-5, min(5, adjustment))
            if adjustment != 0:
                athletic_stats['Jumping'] += adjustment
                athletic_stats['Heading'] += adjustment
                athletic_stats['Physical Power'] += adjustment
                athletic_stats['Speed'] -= adjustment
                athletic_stats['Acceleration'] -= adjustment
            if adjustment < 0 and self.position not in ['Defender', 'Goalkeeper', 'FullBack']:
                # Increase Dribbling for non-defenders
                athletic_stats['Dribbling'] -= adjustment  # Negative adjustment is positive here

        # Ensure stats are within valid ranges
        for stat in athletic_stats:
            athletic_stats[stat] = max(1, min(99, athletic_stats.get(stat, 50)))

    def apply_preferred_foot_adjustments(self, player_stats):
        weak_foot_level = self.preferred_foot['Weak Foot Level']
        if weak_foot_level == 3:
            # Ambidextrous
            player_stats['Attack']['Finishing'] += 5
            player_stats['Attack']['Long Shots'] += 5
            player_stats['Athletic']['Dribbling'] += 5

    # In PlayersStats/player.py

    def additional_calculations(self, player_stats):
        athletic_stats = player_stats['Athletic']

        # Correlate Jumping & Heading
        athletic_stats['Heading'] = self.generate_stat(athletic_stats['Jumping'], 4)

        # Balancing logic
        speed_stats = [
            athletic_stats.get('Speed', 50),
            athletic_stats.get('Acceleration', 50),
            athletic_stats.get('Dribbling', 50)
        ]
        heading_stats = [
            athletic_stats.get('Jumping', 50),
            athletic_stats.get('Heading', 50)
        ]

        if all(stat < 50 for stat in speed_stats):
            athletic_stats['Jumping'] = max(athletic_stats['Jumping'], 65)
            athletic_stats['Heading'] = max(athletic_stats['Heading'], 65)
        elif all(stat < 50 for stat in heading_stats):
            athletic_stats['Speed'] = max(athletic_stats['Speed'], 65)
            athletic_stats['Acceleration'] = max(athletic_stats['Acceleration'], 65)
            if self.position not in ['Defender', 'Goalkeeper', 'FullBack']:
                athletic_stats['Dribbling'] = max(athletic_stats['Dribbling'], 60)
            else:
                athletic_stats['Dribbling'] = max(athletic_stats['Dribbling'], 55)

        # Adjust Physical Power
        if athletic_stats['Jumping'] > 65:
            athletic_stats['Physical Power'] = max(athletic_stats['Physical Power'], 65)

        if athletic_stats['Acceleration'] < 57 or athletic_stats['Speed'] < 57:
            athletic_stats['Physical Power'] = self.generate_stat(70, 4)

        # Correlate Free Kicks and Penalty with other stats
        # Safely get the stat categories
        attack_stats = player_stats.get('Attack', {})
        playmaking_stats = player_stats.get('Playmaking', {})
        set_pieces = player_stats.get('Set Pieces', {})

        # Check if the stats exist before accessing them
        if attack_stats and set_pieces:
            if attack_stats.get('Finishing', 0) > 70 or attack_stats.get('Off The Ball', 0) > 70:
                if 'Penalty' in set_pieces:
                    set_pieces['Penalty'] += 5

            if attack_stats.get('Long Shots', 0) > 70 or playmaking_stats.get('Passing', 0) > 70:
                if 'Free Kicks' in set_pieces:
                    set_pieces['Free Kicks'] += 5

    def calculate_averages(self):
        averages = {}
        for category, stats in self.stats.items():
            avg = sum(stats.values()) / len(stats)
            averages[category] = round(avg)
        return averages

    # Convert the player object to a dictionary for easy output
    def to_dict(self):
        return {
            'Name': self.name,
            'Shirt_Number': self.shirt_number,
            'Position': self.position,
            "Level": self.level,
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
