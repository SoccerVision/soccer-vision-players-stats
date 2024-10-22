# app/core/positions/normal/positions/goalkeeper.py

import random
from app.dep_core.levels.normal.player import Player

class Goalkeeper(Player):
    def __init__(self,assigned_numbers: set = None):
        super().__init__('Goalkeeper', assigned_numbers=assigned_numbers)

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
        stat_config = super().get_stat_config()

        # Goalkeeper-specific stats
        stat_config['Goalkeeping'] = {
            'Aerial Ability': {'mean': 70, 'std_dev': 4},
            'Handling': {'mean': 75, 'std_dev': 4},
            'Kicking': {'mean': 60, 'std_dev': 4},
            'One on One': {'mean': 72, 'std_dev': 4},  # New stat added
            'Reflexes': {'mean': 75, 'std_dev': 4},
        }

        # Remove irrelevant stats
        stat_config.pop('Attack', None)
        stat_config.pop('Playmaking', None)
        stat_config.pop('Defense', None)
        
        # Ensure 'Set Pieces' exists with default values
        stat_config['Set Pieces'] = {
            'Free Kicks': {'mean': 30, 'std_dev': 5, 'min': 20, 'max': 50},
            'Penalty': {'mean': 30, 'std_dev': 5, 'min': 20, 'max': 50},
        }

        # Athletic adjustments
        stat_config['Athletic']['Physical Power']['mean'] = 70
        stat_config['Athletic']['Jumping']['mean'] = 70
        stat_config['Athletic']['Acceleration']['mean'] = 55
        stat_config['Athletic']['Speed'] = {'mean': 55, 'std_dev': 8}
        stat_config['Athletic']['Dribbling']['mean'] = 40
        stat_config['Athletic']['Ball Control']['mean'] = 50

        return stat_config