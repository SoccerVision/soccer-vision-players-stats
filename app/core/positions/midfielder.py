import random
from app.core.player import Player
from app.core.levels.player_config import player_config

class Midfielder(Player):
    def __init__(self, level='normal', assigned_numbers: set = None):
        super().__init__(position='Midfielder', level=level, assigned_numbers=assigned_numbers)

    def get_stat_config(self):
        base_stats = player_config['levels'].get(self.level, {})
        position_stats = player_config['positions'][self.level].get('Midfielder', {})
        return self.merge_configs(base_stats, position_stats)

    def generate_stats(self):
        player_stats = super().generate_stats()  # Get the base stats
        boost_type = self.get_boost_type()

        level_configs = {
            'weaker': {
                'attack_boost': 1.35,
                'defense_boost': 1.45,
            },
            'normal': {
                'attack_boost': 1.35,
                'defense_boost': 1.45,
            },
            'excellent': {
                'attack_boost': 1.20,
                'defense_boost': 1.25,
            },
        }

        if boost_type == 'attack_boost':
            self.apply_attack_boost(player_stats,level_configs)
        elif boost_type == 'defense_boost':
            self.apply_defense_boost(player_stats,level_configs)

        return player_stats

    def get_boost_type(self):
        boost_type = random.choices(
            ['attack_boost', 'defense_boost', 'no_boost'],
            weights=[25, 25, 50],  # 25% for attack, 25% for defense, 50% no boost
            k=1
        )[0]
        return boost_type

    def apply_attack_boost(self, player_stats,level_configs):
        # Apply an attack boost to the player's stats
        attack_boost = level_configs[self.level].get('attack_boost', 1)
        for stat_name in player_stats['Attack']:
            original_value = player_stats['Attack'][stat_name]
            player_stats['Attack'][stat_name] = self.cap_stat(round(original_value * attack_boost), 99)

    def apply_defense_boost(self, player_stats,level_configs):
        # Apply a defense boost to the player's stats
        defense_boost = level_configs[self.level].get('defense_boost', 1)
        for stat_name in player_stats['Defense']:
            original_value = player_stats['Defense'][stat_name]
            player_stats['Defense'][stat_name] = self.cap_stat(round(original_value * defense_boost), 99)
