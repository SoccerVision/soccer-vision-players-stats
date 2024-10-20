# app/core/levels/excellent/positions/winger.py

import random
from app.core.levels.excellent.excellent_player import ExcellentPlayer

class Winger(ExcellentPlayer):
    def __init__(self,assigned_numbers: set = None):
        super().__init__('Winger',assigned_numbers=assigned_numbers)

    def assign_height(self):
        # Lower base height for wingers to 175 cm
        while True:
            height = random.gauss(175, 4)
            if 165 <= height <= 185:
                return round(height)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Winger-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 75, 'std_dev': 6}
        stat_config['Athletic']['Physical Power']['mean'] = 70

        stat_config['Athletic']['Ball Control']['mean'] = 85
        stat_config['Athletic']['Jumping']['mean'] = 75
        stat_config['Athletic']['Speed'] = {'mean': 90, 'std_dev': 8}
        stat_config['Athletic']['Acceleration']['mean'] = 90

        stat_config['Athletic']['Dribbling'] = {
            'mean': (stat_config['Athletic']['Speed']['mean'] + stat_config['Athletic']['Acceleration']['mean']) // 2,
            'std_dev': 5}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 35, 'std_dev': 4},
            'Marking': {'mean': 35, 'std_dev': 4},
            'Positioning': {'mean': 55, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 85, 'std_dev': 4},
            'Long Shots': {'mean': 85, 'std_dev': 4},
            'Off The Ball': {'mean': 90, 'std_dev': 4},
        }

        # Playmaking
        stat_config['Playmaking'] = {
            'Creative': {'mean': 85, 'std_dev': 4},
            'Passing': {'mean': 90, 'std_dev': 4},
            'Crossing': {'mean': 95, 'std_dev': 4}
        }

        return stat_config