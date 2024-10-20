# app/core/levels/normal/positions/midfielder.py

import random
from app.core.levels.normal.player import Player

class Midfielder(Player):
    def __init__(self, assigned_numbers: set = None):
        super().__init__('Midfielder',  assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        stat_config = super().get_stat_config()

        # Midfielder-specific adjustments
        stat_config['Playmaking']['Creative'] = {'mean': 70, 'std_dev': 4}
        stat_config['Playmaking']['Passing'] = {'mean': 72, 'std_dev': 4}
        stat_config['Playmaking']['Crossing'] = {'mean': 70, 'std_dev': 4}

        stat_config['Attack']['Finishing'] = {'mean': 50, 'std_dev': 4}
        stat_config['Attack']['Long Shots'] = {'mean': 60, 'std_dev': 4}
        stat_config['Attack']['Off The Ball'] = {'mean': 55, 'std_dev': 4}

        return stat_config

    def generate_stats(self):
        player_stats = super().generate_stats()  # Get the base stats

        # Apply the 25%-25%-50% logic for boost distribution
        boost_type = random.choices(
            ['attack_boost', 'defense_boost', 'no_boost'],
            weights=[25, 25, 50],  # 25% for attack, 25% for defense, 50% no boost
            k=1
        )[0]

        if boost_type == 'attack_boost':
            self.apply_attack_boost(player_stats)
        elif boost_type == 'defense_boost':
            self.apply_defense_boost(player_stats)

        return player_stats

    def apply_attack_boost(self, player_stats):
        for stat_name in player_stats['Attack']:
            original_value = player_stats['Attack'][stat_name]
            player_stats['Attack'][stat_name] = round(original_value * 1.35)  # 35% boost

    def apply_defense_boost(self, player_stats):
        for stat_name in player_stats['Defense']:
            original_value = player_stats['Defense'][stat_name]
            player_stats['Defense'][stat_name] = round(original_value * 1.45)  # 45% boost
