import random
from app.core.player import Player
from app.core.levels.player_config import player_config


class Fullback(Player):
    def __init__(self, level='normal', dominant_foot=None, assigned_numbers: set = None, ):
        self.forced_dominant_foot = dominant_foot  # Store the forced dominant foot
        super().__init__('FullBack', level=level, assigned_numbers=assigned_numbers)

    def assign_preferred_foot(self):
        if self.forced_dominant_foot:
            # Use the forced dominant foot
            dominant_foot = self.forced_dominant_foot
        else:
            # FullBack-specific dominant foot probabilities: 60% Right, 40% Left
            dominant_foot = random.choices(
                ['Right', 'Left'],
                weights=[60, 40],
                k=1
            )[0]
        # Weaker foot level remains the same
        if random.random() < 0.01:  # 1% chance for ambidextrous
            weaker_foot_level = 3
        else:
            weaker_foot_level = random.choices(
                [1, 2],
                weights=[70, 30],
                k=1
            )[0]
        return {
            'Dominant Foot': dominant_foot,
            'Weak Foot Level': weaker_foot_level
        }

    def get_stat_config(self):
        base_stats = player_config['levels'].get(self.level, {})
        position_stats = player_config['positions'][self.level].get('FullBack', {})
        return self.merge_configs(base_stats, position_stats)
