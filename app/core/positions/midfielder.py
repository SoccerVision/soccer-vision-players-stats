# PlayersStats/Normal/midfielder.py

from ..player import Player

class Midfielder(Player):
    def __init__(self,assigned_numbers: set = None):
        super().__init__('Midfielder',assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Midfielder-specific adjustments
        stat_config['Playmaking']['Creative'] = {'mean': 70, 'std_dev': 4}
        stat_config['Playmaking']['Passing'] = {'mean': 72, 'std_dev': 4}
        stat_config['Playmaking']['Crossing'] = {'mean': 68, 'std_dev': 4}

        stat_config['Attack']['Finishing'] = {'mean': 50, 'std_dev': 4}
        stat_config['Attack']['Long Shots'] = {'mean': 60, 'std_dev': 4}
        stat_config['Attack']['Off The Ball'] = {'mean': 55, 'std_dev': 4}

        return stat_config