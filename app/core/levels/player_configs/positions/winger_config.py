from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

winger_stats = {
    "weaker": {
        **weaker_adjustments,
        'Mental': {
            **weaker_adjustments["Mental"],
            'Composure': {'mean': 40, 'std_dev': 6},
        },
        'Defense': {
            **weaker_adjustments["Defense"],
            'Tackling': {'mean': 25, 'std_dev': 4},
            'Marking': {'mean': 25, 'std_dev': 4},
            'Positioning': {'mean': 45, 'std_dev': 4},
        },
        'Attack': {
            **weaker_adjustments["Attack"],
            'Finishing': {'mean': 50, 'std_dev': 4},
            'Long Shots': {'mean': 50, 'std_dev': 4},
            'Off The Ball': {'mean': 55, 'std_dev': 4},
        },
        'Playmaking': {
            **weaker_adjustments["Playmaking"],
            'Creative': {'mean': 50, 'std_dev': 4},
            'Passing': {'mean': 55, 'std_dev': 4},
            'Crossing': {'mean': 60, 'std_dev': 4}
        },
        'Athletic': {
            **weaker_adjustments["Athletic"],
            'Physical Power': {'mean': 35, 'std_dev': 8},
            'Ball Control': {'mean': 35, 'std_dev': 4},
            'Dribbling': {'mean': 55, 'std_dev': 5},  # !! Calculation !! (Speed+Acceleration)/2=Dribbling
            'Jumping': {'mean': 40, 'std_dev': 8},
            'Acceleration': {'mean': 55, 'std_dev': 8},
            'Speed': {'mean': 55, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        'Mental': {
            **normal_adjustments["Mental"],
            'Composure': {'mean': 55, 'std_dev': 6},
        },
        'Defense': {
            **normal_adjustments["Defense"],
            'Tackling': {'mean': 30, 'std_dev': 4},
            'Marking': {'mean': 30, 'std_dev': 4},
            'Positioning': {'mean': 50, 'std_dev': 4},
        },
        'Attack': {
            **normal_adjustments["Attack"],
            'Finishing': {'mean': 65, 'std_dev': 4},
            'Long Shots': {'mean': 65, 'std_dev': 4},
            'Off The Ball': {'mean': 70, 'std_dev': 4},
        },
        'Playmaking': {
            **normal_adjustments["Playmaking"],
            'Creative': {'mean': 65, 'std_dev': 4},
            'Passing': {'mean': 70, 'std_dev': 4},
            'Crossing': {'mean': 75, 'std_dev': 4}
        },
        'Athletic': {
            **normal_adjustments["Athletic"],
            'Physical Power': {'mean': 50, 'std_dev': 8},
            'Ball Control': {'mean': 65, 'std_dev': 4},
            'Dribbling': {'mean': 70, 'std_dev': 4},  # !! Calculation !! (Speed+Acceleration)/2=Dribbling
            'Jumping': {'mean': 55, 'std_dev': 8},
            'Acceleration': {'mean': 70, 'std_dev': 8},
            'Speed': {'mean': 70, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'Mental': {
            **excellent_adjustments["Mental"],
            'Composure': {'mean': 75, 'std_dev': 6},
        },
        'Defense': {
            **excellent_adjustments["Defense"],
            'Tackling': {'mean': 35, 'std_dev': 4},
            'Marking': {'mean': 35, 'std_dev': 4},
            'Positioning': {'mean': 55, 'std_dev': 4},
        },
        'Attack': {
            **excellent_adjustments["Attack"],
            'Finishing': {'mean': 85, 'std_dev': 4},
            'Long Shots': {'mean': 85, 'std_dev': 4},
            'Off The Ball': {'mean': 90, 'std_dev': 4},
        },
        'Playmaking': {
            **excellent_adjustments["Playmaking"],
            'Creative': {'mean': 85, 'std_dev': 4},
            'Passing': {'mean': 90, 'std_dev': 4},
            'Crossing': {'mean': 95, 'std_dev': 4}
        },
        'Athletic': {
            **excellent_adjustments["Athletic"],
            'Physical Power': {'mean': 70, 'std_dev': 8},
            'Ball Control': {'mean': 85, 'std_dev': 4},
            'Dribbling': {'mean': 90, 'std_dev': 4},  # !! Calculation !! (Speed+Acceleration)/2=Dribbling
            'Jumping': {'mean': 75, 'std_dev': 8},
            'Acceleration': {'mean': 90, 'std_dev': 8},
            'Speed': {'mean': 90, 'std_dev': 8},
        },
    }
}
