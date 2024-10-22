# app/core/positions/excellent/positions/striker.py

from app.dep_core.levels.excellent.excellent_player import ExcellentPlayer

class Striker(ExcellentPlayer):
    def __init__(self,assigned_numbers: set = None,):
        super().__init__('Striker', assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Striker-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 90, 'std_dev': 4}
        stat_config['Athletic']['Physical Power']['mean'] = 75
        stat_config['Athletic']['Ball Control']['mean'] = 80
        stat_config['Athletic']['Dribbling']['mean'] = 85
        stat_config['Athletic']['Jumping']['mean'] = 75
        stat_config['Athletic']['Acceleration']['mean'] = 85
        stat_config['Athletic']['Speed'] = {'mean': 85, 'std_dev': 8}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 35, 'std_dev': 4},
            'Marking': {'mean': 35, 'std_dev': 4},
            'Positioning': {'mean': 40, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 95, 'std_dev': 4},
            'Long Shots': {'mean': 90, 'std_dev': 4},
            'Off The Ball': {'mean': 90, 'std_dev': 4},
        }

        return stat_config