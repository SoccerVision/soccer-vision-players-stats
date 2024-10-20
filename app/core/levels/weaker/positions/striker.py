# app/core/levels/weaker/positions/striker.py

from app.core.levels.weaker.weaker_player import WeakerPlayer

class Striker(WeakerPlayer):
    def __init__(self,assigned_numbers: set = None):
        super().__init__('Striker', assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Striker-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 50, 'std_dev': 4}
        stat_config['Athletic']['Physical Power']['mean'] = 35
        stat_config['Athletic']['Ball Control']['mean'] = 40
        stat_config['Athletic']['Dribbling']['mean'] = 45
        stat_config['Athletic']['Jumping']['mean'] = 35
        stat_config['Athletic']['Acceleration']['mean'] = 45
        stat_config['Athletic']['Speed'] = {'mean': 45, 'std_dev': 8}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 15, 'std_dev': 4},
            'Marking': {'mean': 15, 'std_dev': 4},
            'Positioning': {'mean': 20, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 55, 'std_dev': 4},
            'Long Shots': {'mean': 50, 'std_dev': 4},
            'Off The Ball': {'mean': 50, 'std_dev': 4},
        }

        return stat_config