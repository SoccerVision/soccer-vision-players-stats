# PlayersStats/Normal/defender.py

from ..player import Player

class Defender(Player):
    def __init__(self, assigned_numbers: set = None):
        super().__init__('Defender',assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Defender-specific adjustments
        stat_config['Mental']['Composure'] = {'mean': 50, 'std_dev': 6}
        stat_config['Athletic']['Physical Power']['mean'] = 65
        stat_config['Athletic']['Ball Control']['mean'] = 55
        stat_config['Athletic']['Dribbling']['mean'] = 50
        stat_config['Athletic']['Jumping']['mean'] = 65
        stat_config['Athletic']['Acceleration']['mean'] = 65
        stat_config['Athletic']['Speed'] = {'mean': 65, 'std_dev': 8}

        # Defense stats
        stat_config['Defense'] = {
            'Tackling': {'mean': 75, 'std_dev': 4},
            'Marking': {'mean': 75, 'std_dev': 4},
            'Positioning': {'mean': 70, 'std_dev': 4},
        }

        # Attack stats
        stat_config['Attack'] = {
            'Finishing': {'mean': 25, 'std_dev': 4},
            'Long Shots': {'mean': 25, 'std_dev': 4},
            'Off The Ball': {'mean': 30, 'std_dev': 4},
        }

        return stat_config