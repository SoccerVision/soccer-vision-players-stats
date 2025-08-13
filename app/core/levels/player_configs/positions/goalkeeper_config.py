from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

goalkeeper_stats = {
    "weaker": {
        **weaker_adjustments,
        'mental': {
            **weaker_adjustments["mental"],
            'composure': {'mean': 35, 'std_dev': 6},
        },
        'set_pieces': {
            **weaker_adjustments["set_pieces"],
            'free_kicks': {'mean': 20, 'std_dev': 5, 'min': 20, 'max': 55},
            'penalty': {'mean': 20, 'std_dev': 5, 'min': 20, 'max': 55},
        },
        'goalkeeping': {
            'aerial_ability': {'mean': 55, 'std_dev': 4},
            'handling': {'mean': 60, 'std_dev': 4},
            'kicking': {'mean': 45, 'std_dev': 4},
            'one_on_one': {'mean': 57, 'std_dev': 4},
            'reflexes': {'mean': 42, 'std_dev': 4},
        },
        'athletic': {
            **weaker_adjustments["athletic"],
            'physical_power': {'mean': 55, 'std_dev': 8},
            'ball_control': {'mean': 35, 'std_dev': 4},
            'dribbling': {'mean': 25, 'std_dev': 4},
            'jumping': {'mean': 55, 'std_dev': 8},
            'acceleration': {'mean': 40, 'std_dev': 8},
            'speed': {'mean': 40, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        'set_pieces': {
            **normal_adjustments["set_pieces"],
            'free_kicks': {'mean': 30, 'std_dev': 5, 'min': 20, 'max': 50},
            'penalty': {'mean': 30, 'std_dev': 5, 'min': 20, 'max': 50},
        },
        "goalkeeping": {
            'aerial_ability': {'mean': 70, 'std_dev': 4},
            'handling': {'mean': 75, 'std_dev': 4},
            'kicking': {'mean': 60, 'std_dev': 4},
            'one_on_one': {'mean': 72, 'std_dev': 4},
            'reflexes': {'mean': 75, 'std_dev': 4},
        },
        'athletic': {
            **normal_adjustments["athletic"],
            'physical_power': {'mean': 70, 'std_dev': 8},
            'ball_control': {'mean': 50, 'std_dev': 4},
            'dribbling': {'mean': 40, 'std_dev': 4},
            'jumping': {'mean': 70, 'std_dev': 8},
            'acceleration': {'mean': 55, 'std_dev': 8},
            'speed': {'mean': 55, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'goalkeeping': {
            'aerial_ability': {'mean': 90, 'std_dev': 4},
            'handling': {'mean': 95, 'std_dev': 4},
            'kicking': {'mean': 80, 'std_dev': 4},
            'one_on_one': {'mean': 92, 'std_dev': 4},
            'reflexes': {'mean': 95, 'std_dev': 4},
        },
        "set_pieces": {
            **excellent_adjustments["set_pieces"],
            'free_kicks': {'mean': 50, 'std_dev': 5, 'min': 20, 'max': 70},
            'penalty': {'mean': 50, 'std_dev': 5, 'min': 20, 'max': 70},
        },
        'athletic': {
            **excellent_adjustments["athletic"],
            'physical_power': {'mean': 90, 'std_dev': 8},
            'ball_control': {'mean': 70, 'std_dev': 4},
            'dribbling': {'mean': 60, 'std_dev': 4},
            'jumping': {'mean': 90, 'std_dev': 8},
            'acceleration': {'mean': 75, 'std_dev': 8},
            'speed': {'mean': 75, 'std_dev': 8},
        },
    }
}
