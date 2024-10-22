from app.core.player import Player
from app.core.levels.player_config import player_config


class Striker(Player):
    def __init__(self, level='normal', assigned_numbers: set = None, ):
        super().__init__('Striker', level=level, assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        base_stats = player_config['levels'].get(self.level, {})
        position_stats = player_config['positions'][self.level].get('Striker', {})
        return self.merge_configs(base_stats, position_stats)
