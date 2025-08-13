from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

fullback_stats = {
    "weaker": {
        **weaker_adjustments,
        'mental': {
            **weaker_adjustments["mental"],
            'composure': {'mean': 40, 'std_dev': 6},
        },
        "defense": {
            **weaker_adjustments["defense"],
            "tackling": {"mean": 55, "std_dev": 4},
            "marking": {"mean": 55, "std_dev": 4},
            "positioning": {"mean": 50, "std_dev": 4},
        },
        'attack': {
            **weaker_adjustments["attack"],
            'finishing': {'mean': 30, 'std_dev': 4},
            'long_shots': {'mean': 35, 'std_dev': 4},
            'off_the_ball': {'mean': 45, 'std_dev': 4},
        },
        'playmaking': {
            **weaker_adjustments["playmaking"],
            'crossing': {'mean': 50, 'std_dev': 4},
        },
        'athletic': {
            **weaker_adjustments["athletic"],
            'physical_power': {'mean': 45, 'std_dev': 6},
            'ball_control': {'mean': 45, 'std_dev': 4},
            'dribbling': {'mean': 45, 'std_dev': 4},
            'jumping': {'mean': 45, 'std_dev': 8},
            'acceleration': {'mean': 54, 'std_dev': 8},
            'speed': {'mean': 55, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        "mental": {
            **normal_adjustments["mental"],
            'composure': {'mean': 55, 'std_dev': 6},
        },
        "playmaking": {
            **normal_adjustments["playmaking"],
            'crossing': {'mean': 70, 'std_dev': 4},
        },
        'defense': {
            **normal_adjustments["defense"],
            'tackling': {'mean': 70, 'std_dev': 4},
            'marking': {'mean': 70, 'std_dev': 4},
            'positioning': {'mean': 65, 'std_dev': 4},
        },
        'attack': {
            **normal_adjustments["attack"],
            'finishing': {'mean': 35, 'std_dev': 4},
            'long_shots': {'mean': 40, 'std_dev': 4},
            'off_the_ball': {'mean': 50, 'std_dev': 4},
        },
        'athletic': {
            **normal_adjustments["athletic"],
            'physical_power': {'mean': 60, 'std_dev': 8},
            'ball_control': {'mean': 60, 'std_dev': 4},
            'dribbling': {'mean': 60, 'std_dev': 4},
            'jumping': {'mean': 60, 'std_dev': 8},
            'acceleration': {'mean': 70, 'std_dev': 8},
            'speed': {'mean': 70, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        "mental": {
            **excellent_adjustments["mental"],
            'composure': {'mean': 55, 'std_dev': 6},
        },
        "playmaking": {
            **excellent_adjustments["playmaking"],
            'crossing': {'mean': 70, 'std_dev': 4},
        },
        'defense': {
            **excellent_adjustments["defense"],
            'tackling': {'mean': 80, 'std_dev': 4},
            'marking': {'mean': 80, 'std_dev': 4},
            'positioning': {'mean': 75, 'std_dev': 4},
        },
        'attack': {
            **excellent_adjustments["attack"],
            'finishing': {'mean': 35, 'std_dev': 4},
            'long_shots': {'mean': 40, 'std_dev': 4},
            'off_the_ball': {'mean': 50, 'std_dev': 4},
        },
        'athletic': {
            **excellent_adjustments["athletic"],
            'physical_power': {'mean': 60, 'std_dev': 8},
            'ball_control': {'mean': 60, 'std_dev': 4},
            'dribbling': {'mean': 60, 'std_dev': 4},
            'jumping': {'mean': 60, 'std_dev': 8},
            'acceleration': {'mean': 70, 'std_dev': 8},
            'speed': {'mean': 70, 'std_dev': 8},
        },
    }
}
