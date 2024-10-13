import random
import string
import uuid
from typing import Dict, Any

class Player:
    def __init__(self, position: str, assigned_numbers: set = None):
        self.position = position
        self.id = self.assign_id()
        self.name = self.assign_name()
        self.shirt_number = self.assign_shirt_number(assigned_numbers)
        self.age = self.assign_age()
        self.height = self.assign_height()
        self.preferred_foot = self.assign_preferred_foot()
        self.stamina = self.assign_stamina()
        self.fitness = self.assign_fitness()
        self.nationality = self.assign_nationality()
        self.stats = self.generate_stats()
        self.averages = self.calculate_averages()

    def assign_id(self) -> str:
        return str(uuid.uuid4())

    def assign_name(self) -> str:
        first_names = ['John', 'Michael', 'David', 'Chris', 'James', 'Robert', 'Daniel', 'William', 'Richard', 'Thomas']
        last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin']
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        return name

    def assign_shirt_number(self, assigned_numbers: set = None) -> int:
        if assigned_numbers is None:
            assigned_numbers = set()
        available_numbers = set(range(1, 100)) - assigned_numbers
        shirt_number = random.choice(list(available_numbers))
        assigned_numbers.add(shirt_number)
        return shirt_number

    def assign_age(self) -> int:
        return random.randint(18, 35)

    def assign_height(self) -> int:
        return random.randint(165, 195)

    def assign_preferred_foot(self) -> Dict[str, Any]:
        dominant_foot = random.choices(['Right', 'Left'], weights=[75, 25], k=1)[0]
        weaker_foot_level = random.choices([1, 2], weights=[70, 30], k=1)[0]
        return {
            'Dominant Foot': dominant_foot,
            'Weak Foot Level': weaker_foot_level
        }

    def assign_stamina(self) -> int:
        return random.randint(60, 90)

    def assign_fitness(self) -> str:
        return random.choice(['Low', 'Moderate', 'Peak'])

    def assign_nationality(self) -> str:
        return random.choice(['CountryA', 'CountryB', 'CountryC'])

    def generate_stats(self) -> Dict[str, Dict[str, int]]:
        stats = {}
        # 'Mental' and 'Athletic' categories remain the same
        stats['Mental'] = {
            'Aggression': random.randint(40, 80),
            'Composure': random.randint(40, 80),
            'Decisions': random.randint(40, 80),
            'Teamwork': random.randint(40, 80),
        }
        stats['Athletic'] = {
            'Acceleration': random.randint(40, 80),
            'Ball Control': random.randint(40, 80),
            'Dribbling': random.randint(40, 80),
            'Heading': random.randint(40, 80),
            'Jumping': random.randint(40, 80),
            'Physical Power': random.randint(40, 80),
            'Speed': random.randint(40, 80),
        }
        # For the other categories, generate stats based on mean and std_dev
        other_categories = {
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
            'Set Pieces': {
                'Free Kicks': {'mean': 50, 'std_dev': 15, 'min': 30, 'max': 90},
                'Penalty': {'mean': 60, 'std_dev': 15, 'min': 30, 'max': 90},
            },
        }
        for category, stats_dict in other_categories.items():
            stats[category] = {}
            for stat_name, params in stats_dict.items():
                mean = params['mean']
                std_dev = params['std_dev']
                min_val = params.get('min', 0)
                max_val = params.get('max', 100)
                value = int(random.gauss(mean, std_dev))
                # Clamp the value between min_val and max_val
                value = max(min_val, min(max_val, value))
                stats[category][stat_name] = value
        return stats

    def calculate_averages(self) -> Dict[str, int]:
        averages = {}
        for category, stats in self.stats.items():
            avg = sum(stats.values()) / len(stats)
            averages[category] = int(round(avg))
        return averages

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Name': self.name,
            'Shirt_Number': self.shirt_number,
            'Position': self.position,
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