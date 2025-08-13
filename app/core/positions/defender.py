import random
from app.core.player import Player
from app.core.levels.player_config import player_config

class Defender(Player):
    def __init__(self, level='normal', assigned_numbers: set = None):
        super().__init__('defender', level=level, assigned_numbers=assigned_numbers)

    def assign_height(self):
        # Generate height with normal distribution centered at 183 cm
        while True:
            height = random.gauss(183, 4)
            if 175 <= height <= 200:
                # Adjust for rarity of heights below 180 cm
                if height < 180:
                    if random.random() < 0.10:  # 10% chance for heights below 180 cm
                        return round(height)
                else:
                    return round(height)

    def get_stat_config(self):
        return player_config['positions'][self.level].get('defender', {})
