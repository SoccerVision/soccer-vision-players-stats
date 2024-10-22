import random
from app.core.player import Player
from app.core.levels.player_config import player_config


class Winger(Player):
    def __init__(self, level='normal', assigned_numbers: set = None):
        super().__init__('Winger', level=level, assigned_numbers=assigned_numbers)

    def assign_height(self):
        # Lower base height for wingers to 175 cm
        while True:
            height = random.gauss(175, 4)
            if 165 <= height <= 185:
                return round(height)

    def get_stat_config(self):
        base_stats = player_config['levels'].get(self.level, {})
        position_stats = player_config['positions'][self.level].get('Winger', {})
        return self.merge_configs(base_stats, position_stats)
