from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

striker_stats = {
    "weaker": {
        **weaker_adjustments,
        'Mental': {
            **weaker_adjustments["Mental"],
            'Composure': {'mean': 55, 'std_dev': 4},
        },
        'Defense': {
            **weaker_adjustments["Defense"],
            'Tackling': {'mean': 20, 'std_dev': 4},
            'Marking': {'mean': 20, 'std_dev': 4},
            'Positioning': {'mean': 25, 'std_dev': 4},
        },
        'Attack': {
            **weaker_adjustments["Attack"],
            'Finishing': {'mean': 60, 'std_dev': 4},
            'Long Shots': {'mean': 55, 'std_dev': 4},
            'Off The Ball': {'mean': 55, 'std_dev': 4},
        },
        'Athletic': {
            **weaker_adjustments["Athletic"],
            'Physical Power': {'mean': 40, 'std_dev': 8},
            'Ball Control': {'mean': 45, 'std_dev': 4},
            'Dribbling': {'mean': 50, 'std_dev': 4},
            'Jumping': {'mean': 40, 'std_dev': 8},
            'Acceleration': {'mean': 50, 'std_dev': 8},
            'Speed': {'mean': 50, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        'Mental': {
            **normal_adjustments["Mental"],
            'Composure': {'mean': 70, 'std_dev': 4},
        },
        'Defense': {
            **normal_adjustments["Defense"],
            'Tackling': {'mean': 25, 'std_dev': 4},
            'Marking': {'mean': 25, 'std_dev': 4},
            'Positioning': {'mean': 30, 'std_dev': 4},
        },
        'Attack': {
            **normal_adjustments["Attack"],
            'Finishing': {'mean': 75, 'std_dev': 4},
            'Long Shots': {'mean': 70, 'std_dev': 4},
            'Off The Ball': {'mean': 70, 'std_dev': 4},
        },
        'Athletic': {
            **normal_adjustments["Athletic"],
            'Physical Power': {'mean': 55, 'std_dev': 8},
            'Ball Control': {'mean': 60, 'std_dev': 4},
            'Dribbling': {'mean': 65, 'std_dev': 4},
            'Jumping': {'mean': 55, 'std_dev': 8},
            'Acceleration': {'mean': 65, 'std_dev': 8},
            'Speed': {'mean': 65, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'Mental': {
            **excellent_adjustments["Mental"],
            'Composure': {'mean': 90, 'std_dev': 4},
        },
        'Defense': {
            **excellent_adjustments["Defense"],
            'Tackling': {'mean': 35, 'std_dev': 4},
            'Marking': {'mean': 35, 'std_dev': 4},
            'Positioning': {'mean': 45, 'std_dev': 4},
        },
        'Attack': {
            **excellent_adjustments["Attack"],
            'Finishing': {'mean': 95, 'std_dev': 4},
            'Long Shots': {'mean': 90, 'std_dev': 4},
            'Off The Ball': {'mean': 90, 'std_dev': 4},
        },
        'Athletic': {
            **excellent_adjustments["Athletic"],
            'Physical Power': {'mean': 75, 'std_dev': 8},
            'Ball Control': {'mean': 80, 'std_dev': 4},
            'Dribbling': {'mean': 85, 'std_dev': 4},
            'Jumping': {'mean': 75, 'std_dev': 8},
            'Acceleration': {'mean': 85, 'std_dev': 8},
            'Speed': {'mean': 85, 'std_dev': 8},
        },
    }
}
