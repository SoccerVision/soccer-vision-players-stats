from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

striker_stats = {
    "weaker": {
        **weaker_adjustments,
        'mental': {
            **weaker_adjustments["mental"],
            'composure': {'mean': 55, 'std_dev': 4},
        },
        'defense': {
            **weaker_adjustments["defense"],
            'tackling': {'mean': 20, 'std_dev': 4},
            'marking': {'mean': 20, 'std_dev': 4},
            'positioning': {'mean': 25, 'std_dev': 4},
        },
        'attack': {
            **weaker_adjustments["attack"],
            'finishing': {'mean': 60, 'std_dev': 4},
            'long_shots': {'mean': 55, 'std_dev': 4},
            'off_the_ball': {'mean': 55, 'std_dev': 4},
        },
        'athletic': {
            **weaker_adjustments["athletic"],
            'physical_power': {'mean': 40, 'std_dev': 8},
            'ball_control': {'mean': 45, 'std_dev': 4},
            'dribbling': {'mean': 50, 'std_dev': 4},
            'jumping': {'mean': 40, 'std_dev': 8},
            'acceleration': {'mean': 50, 'std_dev': 8},
            'speed': {'mean': 50, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        'mental': {
            **normal_adjustments["mental"],
            'composure': {'mean': 70, 'std_dev': 4},
        },
        'defense': {
            **normal_adjustments["defense"],
            'tackling': {'mean': 25, 'std_dev': 4},
            'marking': {'mean': 25, 'std_dev': 4},
            'positioning': {'mean': 30, 'std_dev': 4},
        },
        'attack': {
            **normal_adjustments["attack"],
            'finishing': {'mean': 75, 'std_dev': 4},
            'long_shots': {'mean': 70, 'std_dev': 4},
            'off_the_ball': {'mean': 70, 'std_dev': 4},
        },
        'athletic': {
            **normal_adjustments["athletic"],
            'physical_power': {'mean': 55, 'std_dev': 8},
            'ball_control': {'mean': 60, 'std_dev': 4},
            'dribbling': {'mean': 65, 'std_dev': 4},
            'jumping': {'mean': 55, 'std_dev': 8},
            'acceleration': {'mean': 65, 'std_dev': 8},
            'speed': {'mean': 65, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'mental': {
            **excellent_adjustments["mental"],
            'composure': {'mean': 90, 'std_dev': 4},
        },
        'defense': {
            **excellent_adjustments["defense"],
            'tackling': {'mean': 35, 'std_dev': 4},
            'marking': {'mean': 35, 'std_dev': 4},
            'positioning': {'mean': 45, 'std_dev': 4},
        },
        'attack': {
            **excellent_adjustments["attack"],
            'finishing': {'mean': 95, 'std_dev': 4},
            'long_shots': {'mean': 90, 'std_dev': 4},
            'off_the_ball': {'mean': 90, 'std_dev': 4},
        },
        'athletic': {
            **excellent_adjustments["athletic"],
            'physical_power': {'mean': 75, 'std_dev': 8},
            'ball_control': {'mean': 80, 'std_dev': 4},
            'dribbling': {'mean': 85, 'std_dev': 4},
            'jumping': {'mean': 75, 'std_dev': 8},
            'acceleration': {'mean': 85, 'std_dev': 8},
            'speed': {'mean': 85, 'std_dev': 8},
        },
    }
}
