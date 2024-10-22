# # app/core/positions/weaker/positions/winger.py

import random
from app.dep_core.levels.weaker.weaker_player import WeakerPlayer

class Winger(WeakerPlayer):
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
        stat_config['Mental']['Composure'] = {'mean': 40, 'std_dev': 6}
        stat_config['Athletic']['Physical Power']['mean'] = 35

        stat_config['Athletic']['Ball Control']['mean'] = 50
        stat_config['Athletic']['Jumping']['mean'] = 40
        stat_config['Athletic']['Speed'] = {'mean': 55, 'std_dev': 8}
        stat_config['Athletic']['Acceleration']['mean'] = 55

        stat_config['Athletic']['Dribbling'] = {
            'mean': (stat_config['Athletic']['Speed']['mean'] + stat_config['Athletic']['Acceleration']['mean']) // 2,
            'std_dev': 5}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 25, 'std_dev': 4},
            'Marking': {'mean': 25, 'std_dev': 4},
            'Positioning': {'mean': 45, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 50, 'std_dev': 4},
            'Long Shots': {'mean': 50, 'std_dev': 4},
            'Off The Ball': {'mean': 55, 'std_dev': 4},
        }

        # Playmaking
        stat_config['Playmaking'] = {
            'Creative': {'mean': 50, 'std_dev': 4},
            'Passing': {'mean': 55, 'std_dev': 4},
            'Crossing': {'mean': 60, 'std_dev': 4}
        }

        return stat_config