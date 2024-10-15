import random
import uuid
from typing import Dict, Any

class Player:
    def __init__(self, position: str, assigned_numbers: set = None):
        self.position = position
        self.id = self.assign_id()  # Unique player ID
        self.name = self.assign_name()  # Player name
        self.shirt_number = self.assign_shirt_number(assigned_numbers)  # Unique shirt number
        self.age = self.assign_age()  # Player age
        self.height = self.assign_height()  # Player height
        self.preferred_foot = self.assign_preferred_foot()  # Dominant foot and weak foot level
        self.stamina = self.assign_stamina()  # Stamina level
        self.fitness = self.assign_fitness()  # Fitness level (Low, Moderate, Peak)
        self.nationality = self.assign_nationality()  # Player's nationality
        self.stat_config = self.get_stat_config()  # Generate the base stat configuration
        self.stats = self.generate_stats()  # Generate the stats based on configuration
        self.averages = self.calculate_averages()  # Calculate stat averages

    # Assign unique player ID
    def assign_id(self) -> str:
        return str(uuid.uuid4())

    # Generate a random name for the player
    def assign_name(self) -> str:
        first_names = ['John', 'Michael', 'David', 'Chris', 'James', 'Robert', 'Daniel', 'William', 'Richard', 'Thomas']
        last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin']
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    # Assign a unique shirt number to each player
    def assign_shirt_number(self, assigned_numbers: set = None) -> int:
        if assigned_numbers is None:
            assigned_numbers = set()
        available_numbers = set(range(1, 100)) - assigned_numbers
        shirt_number = random.choice(list(available_numbers))
        assigned_numbers.add(shirt_number)
        return shirt_number

    # Assign player age
    def assign_age(self) -> int:
        return random.randint(18, 35)

    # Assign player height
    def assign_height(self) -> int:
        return random.randint(165, 195)

    # Assign dominant and weak foot preferences
    def assign_preferred_foot(self) -> Dict[str, Any]:
        dominant_foot = random.choices(['Right', 'Left'], weights=[75, 25], k=1)[0]
        weaker_foot_level = random.choices([1, 2], weights=[70, 30], k=1)[0]
        return {
            'Dominant Foot': dominant_foot,
            'Weak Foot Level': weaker_foot_level
        }

    # Assign stamina
    def assign_stamina(self) -> int:
        return random.randint(60, 90)

    # Assign fitness level
    def assign_fitness(self) -> str:
        return random.choice(['Low', 'Moderate', 'Peak'])

    # Assign nationality
    def assign_nationality(self) -> str:
        return random.choice(['CountryA', 'CountryB', 'CountryC'])

    # Method to define the base stats configuration for all players
    def get_stat_config(self) -> Dict[str, Any]:
        return {
            'Mental': {
                'Aggression': {'mean': 50, 'std_dev': 15, 'min': 10, 'max': 90},
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

    # Generate individual stats based on the stat configuration
    def generate_stats(self) -> Dict[str, Dict[str, int]]:
        stats = {}
        for category, stats_dict in self.stat_config.items():
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

    # Calculate the average of the stats per category
    def calculate_averages(self) -> Dict[str, int]:
        averages = {}
        for category, stats in self.stats.items():
            avg = sum(stats.values()) / len(stats)
            averages[category] = int(round(avg))
        return averages

    # Convert the player object to a dictionary for easy output
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