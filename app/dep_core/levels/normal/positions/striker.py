# app/core/positions/normal/positions/striker.py

from app.dep_core.levels.normal.player import Player

class Striker(Player):
    def __init__(self,assigned_numbers: set = None,):
        super().__init__('Striker', assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Striker-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 70, 'std_dev': 4}
        stat_config['Athletic']['Physical Power']['mean'] = 55
        stat_config['Athletic']['Ball Control']['mean'] = 60
        stat_config['Athletic']['Dribbling']['mean'] = 65
        stat_config['Athletic']['Jumping']['mean'] = 55
        stat_config['Athletic']['Acceleration']['mean'] = 65
        stat_config['Athletic']['Speed'] = {'mean': 65, 'std_dev': 8}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 25, 'std_dev': 4},
            'Marking': {'mean': 25, 'std_dev': 4},
            'Positioning': {'mean': 30, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 75, 'std_dev': 4},
            'Long Shots': {'mean': 70, 'std_dev': 4},
            'Off The Ball': {'mean': 70, 'std_dev': 4},
        }

        return stat_config