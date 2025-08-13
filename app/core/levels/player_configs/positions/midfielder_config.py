from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

midfielder_stats = {
    "weaker": {
        **weaker_adjustments,
        'attack': {
            **weaker_adjustments["attack"],
            'finishing': {'mean': 35, 'std_dev': 4},
            'long_shots': {'mean': 45, 'std_dev': 4},
            'off_the_ball': {'mean': 40, 'std_dev': 4},
        },
        'playmaking': {
            **weaker_adjustments["playmaking"],
            'creative': {'mean': 55, 'std_dev': 4},
            'passing': {'mean': 57, 'std_dev': 4},
            'crossing': {'mean': 55, 'std_dev': 4},
        },
    },
    "normal": {
        **normal_adjustments,
        'attack': {
            **normal_adjustments["attack"],
            'finishing': {'mean': 50, 'std_dev': 4},
            'long_shots': {'mean': 60, 'std_dev': 4},
            'off_the_ball': {'mean': 55, 'std_dev': 4},
        },
        'playmaking': {
            **normal_adjustments["playmaking"],
            'creative': {'mean': 70, 'std_dev': 4},
            'passing': {'mean': 72, 'std_dev': 4},
            'crossing': {'mean': 70, 'std_dev': 4},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'attack': {
            **excellent_adjustments["attack"],
            'finishing': {'mean': 70, 'std_dev': 4},
            'long_shots': {'mean': 80, 'std_dev': 4},
            'off_the_ball': {'mean': 75, 'std_dev': 4},
        },
        'playmaking': {
            **excellent_adjustments["playmaking"],
            'creative': {'mean': 90, 'std_dev': 4},
            'passing': {'mean': 92, 'std_dev': 4},
            'crossing': {'mean': 90, 'std_dev': 4},
        },
    }
}
