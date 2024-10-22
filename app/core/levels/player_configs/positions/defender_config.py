from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

defender_stats = {
    "weaker": {
        **weaker_adjustments,
        'Mental': {
            **weaker_adjustments["Mental"],
            'Composure': {'mean': 35, 'std_dev': 6},
        },
        "Defense": {
            **weaker_adjustments["Defense"],
            "Tackling": {"mean": 60, "std_dev": 4},
            "Marking": {"mean": 60, "std_dev": 4},
            "Positioning": {"mean": 55, "std_dev": 4},
        },
        'Attack': {
            **weaker_adjustments["Attack"],
            'Finishing': {'mean': 20, 'std_dev': 4},
            'Long Shots': {'mean': 20, 'std_dev': 4},
            'Off The Ball': {'mean': 25, 'std_dev': 4},
        },
        'Athletic': {
            **weaker_adjustments["Athletic"],
            'Physical Power': {'mean': 50, 'std_dev': 8},
            'Ball Control': {'mean': 40, 'std_dev': 4},
            'Dribbling': {'mean': 35, 'std_dev': 4},
            'Jumping': {'mean': 50, 'std_dev': 8},
            'Acceleration': {'mean': 50, 'std_dev': 8},
            'Speed': {'mean': 50, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        'Defense': {
            **normal_adjustments["Defense"],
            'Tackling': {'mean': 75, 'std_dev': 4},
            'Marking': {'mean': 75, 'std_dev': 4},
            'Positioning': {'mean': 70, 'std_dev': 4},
        },
        'Attack': {
            **normal_adjustments["Attack"],
            'Finishing': {'mean': 25, 'std_dev': 4},
            'Long Shots': {'mean': 25, 'std_dev': 4},
            'Off The Ball': {'mean': 30, 'std_dev': 4},
        },
        'Athletic': {
            **normal_adjustments["Athletic"],
            'Physical Power': {'mean': 65, 'std_dev': 8},
            'Ball Control': {'mean': 55, 'std_dev': 4},
            'Dribbling': {'mean': 50, 'std_dev': 4},
            'Jumping': {'mean': 65, 'std_dev': 8},
            'Acceleration': {'mean': 65, 'std_dev': 8},
            'Speed': {'mean': 65, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'Defense': {
            **excellent_adjustments["Defense"],
            'Tackling': {'mean': 95, 'std_dev': 4},
            'Marking': {'mean': 95, 'std_dev': 4},
            'Positioning': {'mean': 90, 'std_dev': 4},
        },
        'Attack': {
            **excellent_adjustments["Attack"],
            'Finishing': {'mean': 25, 'std_dev': 4},
            'Long Shots': {'mean': 25, 'std_dev': 4},
            'Off The Ball': {'mean': 30, 'std_dev': 4},
        },
        'Athletic': {
            **excellent_adjustments["Athletic"],
            'Physical Power': {'mean': 85, 'std_dev': 8},
            'Ball Control': {'mean': 75, 'std_dev': 4},
            'Dribbling': {'mean': 70, 'std_dev': 4},
            'Jumping': {'mean': 85, 'std_dev': 8},
            'Acceleration': {'mean': 85, 'std_dev': 8},
            'Speed': {'mean': 85, 'std_dev': 8},
        },
    }
}
