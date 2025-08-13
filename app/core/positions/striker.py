from app.core.player import Player
from app.core.levels.player_config import player_config


class Striker(Player):
    def __init__(self, level='normal', assigned_numbers: set = None, ):
        super().__init__('striker', level=level, assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        return player_config['positions'][self.level].get('striker', {})
