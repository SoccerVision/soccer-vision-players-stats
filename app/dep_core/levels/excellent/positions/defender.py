# app/core/levels/excellent/positions/defender.py

import random
from app.dep_core.levels.excellent.excellent_player import ExcellentPlayer

class Defender(ExcellentPlayer):
    def __init__(self, assigned_numbers: set = None):
        super().__init__('Defender',assigned_numbers=assigned_numbers)

    def assign_height(self):
        # Generate height with normal distribution centered at 183 cm
        while True:
            height = random.gauss(183, 4)
            if 175 <= height <= 200:
                # Adjust for rarity of heights below 180 cm
                if height < 180:
                    if random.random() < 0.10:  # 10% chance for heights below 180 cm
                        return round(height)
                else:
                    return round(height)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Defender-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 70, 'std_dev': 6}
        stat_config['Athletic']['Physical Power']['mean'] = 85
        stat_config['Athletic']['Ball Control']['mean'] = 75
        stat_config['Athletic']['Dribbling']['mean'] = 70
        stat_config['Athletic']['Jumping']['mean'] = 85
        stat_config['Athletic']['Acceleration']['mean'] = 85
        stat_config['Athletic']['Speed'] = {'mean': 85, 'std_dev': 8}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 95, 'std_dev': 4},
            'Marking': {'mean': 95, 'std_dev': 4},
            'Positioning': {'mean': 90, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 25, 'std_dev': 4},
            'Long Shots': {'mean': 25, 'std_dev': 4},
            'Off The Ball': {'mean': 30, 'std_dev': 4},
        }

        return stat_config