# app/core/positions/excellent/positions/fullback.py

import random
from app.dep_core.levels.excellent.excellent_player import ExcellentPlayer

class FullBack(ExcellentPlayer):
    def __init__(self, dominant_foot=None,assigned_numbers: set = None,):
        self.forced_dominant_foot = dominant_foot  # Store the forced dominant foot
        super().__init__('FullBack', assigned_numbers=assigned_numbers)

    def assign_preferred_foot(self):
        if self.forced_dominant_foot:
            # Use the forced dominant foot
            dominant_foot = self.forced_dominant_foot
        else:
            # FullBack-specific dominant foot probabilities: 60% Right, 40% Left
            dominant_foot = random.choices(
                ['Right', 'Left'],
                weights=[60, 40],
                k=1
            )[0]
        # Weaker foot level remains the same
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

    def get_stat_config(self):
        stat_config = super().get_stat_config()
        # FullBack-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 55, 'std_dev': 6}
        stat_config['Athletic']['Physical Power']['mean'] = 60
        stat_config['Athletic']['Ball Control']['mean'] = 60
        stat_config['Athletic']['Dribbling']['mean'] = 60
        stat_config['Athletic']['Jumping']['mean'] = 60
        stat_config['Athletic']['Acceleration']['mean'] = 70
        stat_config['Athletic']['Speed'] = {'mean': 70, 'std_dev': 8}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 80, 'std_dev': 4},
            'Marking': {'mean': 80, 'std_dev': 4},
            'Positioning': {'mean': 75, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 35, 'std_dev': 4},
            'Long Shots': {'mean': 40, 'std_dev': 4},
            'Off The Ball': {'mean': 50, 'std_dev': 4},
        }

        # Playmaking
        stat_config['Playmaking']['Crossing'] = {'mean': 70, 'std_dev': 4}

        return stat_config