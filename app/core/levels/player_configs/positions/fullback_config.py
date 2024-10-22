from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

fullback_stats = {
    "weaker": {
        **weaker_adjustments,
        'Mental': {
            **weaker_adjustments["Mental"],
            'Composure': {'mean': 40, 'std_dev': 6},
        },
        "Defense": {
            **weaker_adjustments["Defense"],
            "Tackling": {"mean": 55, "std_dev": 4},
            "Marking": {"mean": 55, "std_dev": 4},
            "Positioning": {"mean": 50, "std_dev": 4},
        },
        'Attack': {
            **weaker_adjustments["Attack"],
            'Finishing': {'mean': 30, 'std_dev': 4},
            'Long Shots': {'mean': 35, 'std_dev': 4},
            'Off The Ball': {'mean': 45, 'std_dev': 4},
        },
        'Playmaking': {
            **weaker_adjustments["Playmaking"],
            'Crossing': {'mean': 50, 'std_dev': 4},
        },
        'Athletic': {
            **weaker_adjustments["Athletic"],
            'Physical Power': {'mean': 45, 'std_dev': 6},
            'Ball Control': {'mean': 45, 'std_dev': 4},
            'Dribbling': {'mean': 45, 'std_dev': 4},
            'Jumping': {'mean': 45, 'std_dev': 8},
            'Acceleration': {'mean': 54, 'std_dev': 8},
            'Speed': {'mean': 55, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        "Mental": {
            **normal_adjustments["Mental"],
            'Composure': {'mean': 55, 'std_dev': 6},
        },
        "Playmaking": {
            **normal_adjustments["Playmaking"],
            'Crossing': {'mean': 70, 'std_dev': 4},
        },
        'Defense': {
            **normal_adjustments["Defense"],
            'Tackling': {'mean': 70, 'std_dev': 4},
            'Marking': {'mean': 70, 'std_dev': 4},
            'Positioning': {'mean': 65, 'std_dev': 4},
        },
        'Attack': {
            **normal_adjustments["Attack"],
            'Finishing': {'mean': 35, 'std_dev': 4},
            'Long Shots': {'mean': 40, 'std_dev': 4},
            'Off The Ball': {'mean': 50, 'std_dev': 4},
        },
        'Athletic': {
            **normal_adjustments["Athletic"],
            'Physical Power': {'mean': 60, 'std_dev': 8},
            'Ball Control': {'mean': 60, 'std_dev': 4},
            'Dribbling': {'mean': 60, 'std_dev': 4},
            'Jumping': {'mean': 60, 'std_dev': 8},
            'Acceleration': {'mean': 70, 'std_dev': 8},
            'Speed': {'mean': 70, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        "Mental": {
            **excellent_adjustments["Mental"],
            'Composure': {'mean': 55, 'std_dev': 6},
        },
        "Playmaking": {
            **excellent_adjustments["Playmaking"],
            'Crossing': {'mean': 70, 'std_dev': 4},
        },
        'Defense': {
            **excellent_adjustments["Defense"],
            'Tackling': {'mean': 80, 'std_dev': 4},
            'Marking': {'mean': 80, 'std_dev': 4},
            'Positioning': {'mean': 75, 'std_dev': 4},
        },
        'Attack': {
            **excellent_adjustments["Attack"],
            'Finishing': {'mean': 35, 'std_dev': 4},
            'Long Shots': {'mean': 40, 'std_dev': 4},
            'Off The Ball': {'mean': 50, 'std_dev': 4},
        },
        'Athletic': {
            **excellent_adjustments["Athletic"],
            'Physical Power': {'mean': 60, 'std_dev': 8},
            'Ball Control': {'mean': 60, 'std_dev': 4},
            'Dribbling': {'mean': 60, 'std_dev': 4},
            'Jumping': {'mean': 60, 'std_dev': 8},
            'Acceleration': {'mean': 70, 'std_dev': 8},
            'Speed': {'mean': 70, 'std_dev': 8},
        },
    }
}
