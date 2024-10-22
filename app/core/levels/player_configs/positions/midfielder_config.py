from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

midfielder_stats = {
    "weaker": {
        **weaker_adjustments,
        'Attack': {
            **weaker_adjustments["Attack"],
            'Finishing': {'mean': 35, 'std_dev': 4},
            'Long Shots': {'mean': 45, 'std_dev': 4},
            'Off The Ball': {'mean': 40, 'std_dev': 4},
        },
        'Playmaking': {
            **weaker_adjustments["Playmaking"],
            'Creative': {'mean': 55, 'std_dev': 4},
            'Passing': {'mean': 57, 'std_dev': 4},
            'Crossing': {'mean': 55, 'std_dev': 4},
        },
    },
    "normal": {
        **normal_adjustments,
        'Attack': {
            **normal_adjustments["Attack"],
            'Finishing': {'mean': 50, 'std_dev': 4},
            'Long Shots': {'mean': 60, 'std_dev': 4},
            'Off The Ball': {'mean': 55, 'std_dev': 4},
        },
        'Playmaking': {
            **normal_adjustments["Playmaking"],
            'Creative': {'mean': 70, 'std_dev': 4},
            'Passing': {'mean': 72, 'std_dev': 4},
            'Crossing': {'mean': 70, 'std_dev': 4},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'Attack': {
            **excellent_adjustments["Attack"],
            'Finishing': {'mean': 70, 'std_dev': 4},
            'Long Shots': {'mean': 80, 'std_dev': 4},
            'Off The Ball': {'mean': 75, 'std_dev': 4},
        },
        'Playmaking': {
            **excellent_adjustments["Playmaking"],
            'Creative': {'mean': 90, 'std_dev': 4},
            'Passing': {'mean': 92, 'std_dev': 4},
            'Crossing': {'mean': 90, 'std_dev': 4},
        },
    }
}
